# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
	# Base box to build off, and download URL for when it doesn't exist on the user's system already
	config.vm.box = "ubuntu/xenial64"

	# Boot with a GUI so you can see the screen. (Default is headless)
	# config.vm.boot_mode = :gui

	# Assign this VM to a host only network IP, allowing you to access it
	# via the IP.
	# config.vm.network "33.33.33.10"

	# Forward a port from the guest to the host, which allows for outside
	# computers to access the VM, whereas host only networking does not.
	config.vm.forward_port 8000, 8000
	config.vm.forward_port 4200, 4200

	# Share an additional folder to the guest VM. The first argument is
	# an identifier, the second is the path on the guest to mount the
	# folder, and the third is the path on the host to the actual folder.
	config.vm.share_folder "backend", "/home/ubuntu/backend", "./backend"
	config.vm.share_folder "frontend", "/home/ubuntu/frontend", "./frontend"
	config.vm.share_folder "etc", "/home/ubuntu/etc", "./etc"



	# Enable provisioning with a shell script.
	config.vm.provision :shell, :path => "etc/vagrant-install.sh"
end
