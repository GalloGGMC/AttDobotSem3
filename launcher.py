import typer

app = typer.Typer()

@app.command()
def roboCMD():
    import src.ponderadaCMD

@app.command()
def roboUI():
    import src.ponderadaUI

if __name__ == "__main__":
    app()