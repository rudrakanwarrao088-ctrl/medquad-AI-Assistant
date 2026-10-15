@echo off
setlocal enabledelayedexpansion
title Push MedQuAD AI Assistant to GitHub
echo =======================================================
echo          Push MedQuAD AI Assistant to GitHub
echo =======================================================
echo.

REM Check for git
set "GIT_CMD=git"
if exist ".mingit\cmd\git.exe" (
    set "GIT_CMD=.mingit\cmd\git.exe"
) else (
    where git >nul 2>nul
    if !ERRORLEVEL! neq 0 (
        echo [ERROR] Git is not found.
        pause
        exit /b 1
    )
)

echo Using Git: !GIT_CMD!
echo.

set "REPO_URL=https://github.com/rashikanwarrao-source/medquad-AI-Assistant.git"
echo Target Repository: %REPO_URL%
echo.

echo Staging changes...
!GIT_CMD! add .

echo Creating commit...
!GIT_CMD! commit -m "MedQuAD AI Medical Assistant & Clinical QA" 2>nul

echo.
echo =====================================================================
echo  NOTE: GitHub requires a Personal Access Token (PAT) as password.
echo  Generate a token at: https://github.com/settings/tokens (Select 'repo')
echo =====================================================================
echo.
echo Pushing to GitHub...
!GIT_CMD! push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo =======================================================
    echo   SUCCESS! Your project is now published on GitHub!
    echo =======================================================
) else (
    echo.
    echo [NOTE] If push was rejected, check that your repository URL is correct
    echo and that you have permission to push to it.
)

echo.
pause
