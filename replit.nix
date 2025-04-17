{pkgs}: {
  deps = [
    pkgs.python312Packages.flask
    pkgs.libmysqlclient
    pkgs.libev
  ];
}
