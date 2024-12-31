{
  stdenv,
  writeShellScriptBin,
  pythonApp,
}: let
  app = writeShellScriptBin "app" ''
    ${pythonApp.app.dependencyEnv}/bin/uvicorn 'app.main:app' \
      --host=0.0.0.0 \
      --port=''${PORT:-8000}
  '';

  shell = writeShellScriptBin "shell" ''
    ${pythonApp.app.dependencyEnv}/bin/python
  '';
in
  stdenv.mkDerivation {
    name = "gamepop-discord-bot";
    version = "0.1.0";
    phases = "installPhase fixupPhase";
    installPhase = ''
      mkdir -p $out/bin
      ln -s ${app}/bin/app $out/bin/app
      ln -s ${shell}/bin/shell $out/bin/shell
    '';
  }
