{poetry2nix}: let
  overrides = poetry2nix.overrides.withDefaults (self: super: {
    # none yet
  });
in {
  app = poetry2nix.mkPoetryApplication {
    projectDir = ./..;
    overrides = overrides;
  };

  devEnv = poetry2nix.mkPoetryEnv {
    projectDir = ./..;
    overrides = overrides;
  };
}
