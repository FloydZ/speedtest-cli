with import <nixpkgs> { };
{ pkgs ? import <nixpkgs> { } }:
let 
  myPython = pkgs.python312;
  pythonPackages = pkgs.python312Packages;
  pythonWithPkgs = myPython.withPackages (pythonPkgs: with pythonPkgs; [
    ipython
    pip
    setuptools
    virtualenv
    wheel
  ]);

  # add the needed packages here
  extraBuildInputs = with pkgs; [
    pythonWithPkgs
    pythonPackages.numpy
    pythonPackages.termplotlib
    pythonPackages.plotext
    wget
  ] ++ (lib.optionals pkgs.stdenv.isLinux ([
  ]));
in
import ./python-shell.nix { 
 extraBuildInputs=extraBuildInputs; 
 myPython=myPython;
 pythonWithPkgs=pythonWithPkgs;
}
