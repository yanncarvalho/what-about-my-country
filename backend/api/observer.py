class ObserverDB :

  def save (self) -> None:
    from backend.populate import Populate
    Populate().start()