{
  mkShell,
  poetry,
  python3,
  pythonApp,
}:
mkShell {
  name = "gamepop-discord-bot";

  nativeBuildInputs = [
    python3
    poetry
  ];

  buildInputs = [pythonApp.devEnv];
}
