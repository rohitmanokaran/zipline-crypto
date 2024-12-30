from zipline.utils.compat import ExitStack, contextmanager, wraps

from .iface import PipelineHooks, PIPELINE_HOOKS_CONTEXT_MANAGERS
from .no import NoHooks


def delegating_hooks_method(method_name):
    """Factory function for making DelegatingHooks methods."""
    if method_name in PIPELINE_HOOKS_CONTEXT_MANAGERS:
        # Generate a contextmanager that enters the context of all child hooks.
        @wraps(getattr(PipelineHooks, method_name))
        @contextmanager
        def ctx(self, *args, **kwargs):
            with ExitStack() as stack:
                for hook in self._hooks:
                    sub_ctx = getattr(hook, method_name)(*args, **kwargs)
                    stack.enter_context(sub_ctx)
                yield stack

        return ctx
    else:
        # Generate a method that calls methods of all child hooks.
        @wraps(getattr(PipelineHooks, method_name))
        def method(self, *args, **kwargs):
            for hook in self._hooks:
                sub_method = getattr(hook, method_name)
                sub_method(*args, **kwargs)

        return method


class DelegatingHooks(PipelineHooks):
    """A PipelineHooks that delegates to one or more other hooks.

    Parameters
    ----------
    hooks : list[PipelineHooks]
        Sequence of hooks to delegate to.
    """

    def __new__(cls, hooks):
        if len(hooks) == 0:
            # OPTIMIZATION: Short-circuit to a NoHooks if we don't have any
            # sub-hooks.
            return NoHooks()
        elif len(hooks) == 1:
            # OPTIMIZATION: Unwrap delegation layer if we only have one
            # sub-hook.
            return hooks[0]
        else:
            self = super(DelegatingHooks, cls).__new__(cls)
            self._hooks = hooks
            return self

    # Implement all abstract methods by delegating to corresponding methods on hooks.
    def __init__(self, hooks):
        self._hooks = hooks

    def some_method(self):
        for hook in self._hooks:
            hook.some_method()

    # Dynamically generate all methods declared in PIPELINE_HOOKS_CONTEXT_MANAGERS
    for name in PIPELINE_HOOKS_CONTEXT_MANAGERS:
        locals()[name] = delegating_hooks_method(name)


del delegating_hooks_method
