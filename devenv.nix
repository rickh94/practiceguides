{ pkgs, ... }: {
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = with pkgs; [
    git
    litestream
    ffmpeg
    rustywind
    ruff
  ];

  certificates = [
    "guides.localhost"
  ];

  languages = {
    python = {
      enable = true;
      poetry = {
        enable = true;
        activate.enable = true;
        install.enable = true;
        install.allExtras = true;
      };
    };
    javascript.enable = true;
  };

  services.caddy = {
    enable = true;
    virtualHosts."guides.localhost" = {
      extraConfig = ''
        reverse_proxy :8000
      '';
    };
  };

  scripts.tw.exec = "bun x tailwindcss -i ./static-src/main.css -o ./static/main.css --watch";
  scripts.automigrate.exec = "python app/manage.py makemigrations && python app/manage.py migrate";

  processes = {
    litestream.exec = "${pkgs.litestream}/bin/litestream replicate -config ${./litestream.dev.yml}";
    dev.exec = "cd app && ${pkgs.poetry}/bin/poetry run python manage.py runserver 0.0.0.0:8000";
  };
}
