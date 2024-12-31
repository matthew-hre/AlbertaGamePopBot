final: prev: {
  devShell = prev.callPackage ./devshell.nix {};
  pythonApp = prev.callPackage ./python-app.nix {};
  app = prev.callPackage ./package.nix {};
}
