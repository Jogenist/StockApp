import reflex as rx

class ReflexstocksConfig(rx.Config):
    pass

config = ReflexstocksConfig(
    app_name="reflex_stocks",
    db_url="sqlite:///user.db",
    #env=rx.Env.DEV,
)