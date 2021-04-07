from discord.ext.commands import CheckFailure

class VerificationError(CheckFailure):
  r"""
  Raised when a user attempts to use a command without verifying
  """
  pass
