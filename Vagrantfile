Vagrant.configure("2") do |config|
    # Базовый образ Ubuntu
    config.vm.box = "ubuntu/focal64"
    
    # Проброс портов
    config.vm.network "forwarded_port", guest: 5000, host: 5000
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    
    # Монтирование папки проекта
    config.vm.synced_folder ".", "/vagrant"
    
    # Установка Docker внутри VM
    config.vm.provision "docker" do |d|
      d.pull_images "python:3.9-slim"
      d.pull_images "node:14"
    end
    
    # Настройка ресурсов виртуальной машины
    config.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.cpus = 2
    end
    
    # Скрипт установки зависимостей
    config.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y docker-compose
    SHELL
  end
  