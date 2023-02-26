@echo off

if "%~1"=="clean" goto clean
if "%~1"=="prepare" goto prepare
if "%~1"=="test" goto test
if "%~1"=="docs" goto docs
if "%~1"=="build" goto build
if "%~1"=="publish" goto publish

@echo Please use the following commands:
@echo    %~n0 clean         (for cleaning all output files)
@echo    %~n0 prepare       (for preparing the virtual environments)
@echo    %~n0 test          (for running unit tests)
@echo    %~n0 docs          (for generating the docs)
@echo    %~n0 build         (for building lattehhpel package)
@echo    %~n0 publish       (for publishing lattehhpel package)
goto end

:clean
pushd %~dp0\tools
call clean.cmd
popd
goto end

:prepare
pushd %~dp0\tools
call prepare.cmd
popd
goto end

:test
pushd %~dp0\tools
call test.cmd
popd
goto end

:docs
pushd %~dp0\tools
call docs.cmd
popd
goto end

:build
pushd %~dp0\tools
call build.cmd
popd
goto end

:publish
pushd %~dp0\tools
call publish.cmd
popd
goto end

:end
