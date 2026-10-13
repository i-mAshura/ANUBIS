class AnubisError(Exception):
    """Base exception for all ANUBIS SDK errors."""
    pass


class AnubisAuthError(AnubisError):
    """Raised when authentication, challenge verification, or signature fails."""
    pass


class AnubisPolicyDeniedError(AnubisError):
    """Raised when the ANUBIS Gateway OPA/Rego policy engine denies tool execution."""
    def __init__(self, message: str, tool: str, reason: str):
        super().__init__(message)
        self.tool = tool
        self.reason = reason


class AnubisApprovalRequiredError(AnubisError):
    """Raised when a tool action is held pending human supervisor approval."""
    def __init__(self, message: str, approval_id: str, tool: str, expires_at: str):
        super().__init__(message)
        self.approval_id = approval_id
        self.tool = tool
        self.expires_at = expires_at


class AnubisKillSwitchError(AnubisError):
    """Raised when the agent, instance, task, or principal has been terminated by the kill switch."""
    pass
