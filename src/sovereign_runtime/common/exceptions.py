class SovereignRuntimeError(Exception):
    pass


class CoherenceFailureError(SovereignRuntimeError):
    pass


class EmbodimentGateError(SovereignRuntimeError):
    pass


class QGateFailureError(SovereignRuntimeError):
    pass
