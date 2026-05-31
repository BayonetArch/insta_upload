function info {
  Write-Host "$([char]27)[0;33minfo$([char]27)[0m: $($args[0])"
}

function fatal {
  Write-Host "fatal $([char]27)[0;31merror$([char]27)[0m: $($args[0])"
    Read-Host "Press Enter to exit...."
    exit 1
}

function is_installed {
  $pkg = $($args[0])
    if (Get-Command $pkg -ErrorAction SilentlyContinue) {
      info "$pkg is installed."
        return $true
    }else{
      info "$pkg is not installed"
        return $false
    }
}

function reload_env {
  $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

function install_choco {
  [System.Net.ServicePointManager]::SecurityProtocol = `
    [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
      iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
      reload_env
        if (!(is_installed "choco")) {
          fatal "Choco was not installed successfully" 
        }
}

function choco_install {
  param($pkg,$checkCmd)

  choco install $pkg -y
  $exitCode = $LASTEXITCODE
  if ($exitCode -ne 0) {
    fatal "failed to install $pkg" 
  }

  reload_env
  if (!(is_installed "$checkCmd")){
    fatal "Failed to install $pkg"
  }
}



function install_py_deps {
  python3.14 -m pip install instagrapi   
  $exitCode = $LASTEXITCODE
  if ($exitCode -ne 0) {
    fatal "failed to install instagrapi python package" 
  }
}

function main {
  info "Installing dependencies..."
    if (! (is_installed "choco")) {
      info "installing Chocolatey..."
        install_choco
    }

  if (!(is_installed "python3.14")){
    info "installing python..."
      choco_install "python314" "python3.14"
  }

  if (!(is_installed "ffmpeg" )) {
    info "installing ffmpeg..."
    choco_install "ffmpeg" "ffmpeg"
  }

  info "installing python dependency..."
  install_py_deps
  info "installing dependencies successfull"
  Write-Host "Edit the 'username' and  'password' in './script.py' and run the script with video path to get started."
  Read-Host "Press Enter to exit...."
}

main @args
