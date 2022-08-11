class ObserverDB :
  """ObserverDB class represeting the observer design pattern of a database"""

  def save (self) -> None:
    """trigger a process when new information is saved to a database"""
    from .populate import Populate
    Populate().start()