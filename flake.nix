{
    description = "Flake utils demo";

    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
        flake-utils.url = "github:numtide/flake-utils";
    };

    outputs = { self, nixpkgs, flake-utils }:
        flake-utils.lib.eachDefaultSystem (system:
            let
                pkgs = nixpkgs.legacyPackages.${system};
                python-pkgs = pkgs: with pkgs; [
                    (pkgs.buildPythonPackage rec {
                        pname = "pygrametl";
                        version = "2.8";
                        src = pkgs.fetchPypi {
                            inherit pname version;
                            sha256 = "sha256-DphXiXQYefok7J93nnMI6cv/bb2QvVHhCDQIC7FlDSg=";
                        };
                        doCheck = false;
                        propagatedBuildInputs = [];
                    })
                    psycopg2
                ];
            in {
                packages = rec {
                    default = pkgs.hello;
                };
                devShells.default = pkgs.mkShell {
                    nativeBuildInputs = [
                        (pkgs.python3.withPackages python-pkgs)
                        pkgs.python311Packages.python-lsp-server
                        pkgs.postgresql
                    ];

                    shellHook = ''
                        echo Welcome to distributed systems shell
                    '';
                };
            }
        );
}
