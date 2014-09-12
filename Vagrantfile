Vagrant.configure("2") do |config|
  config.vm.box = 'Phusion-Ubuntu-Server-Precise-14.04-amd64'
  config.vm.box_url = "https://oss-binaries.phusionpassenger.com/" + \
                      "vagrant/boxes/latest/ubuntu-14.04-amd64-vbox.box"
#  config.vm.box = 'precice32'
  config.vm.provision :shell, :path => 'bootstrap.sh'
end
