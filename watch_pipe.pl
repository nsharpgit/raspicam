#!/usr/bin/perl
#open(FILE,">>/root/watch.log");
while(<STDIN>) {
        if ( $_ =~ /webcam control pause camera/ ) {
                #print "matched $_\n";
                system("touch /var/www/webcam/tmp/.pause");
        }
        elsif ( $_ =~ /webcam control start camera/ ) {
                #print "matched $_\n";
                system("rm /var/www/webcam/tmp/.pause");
        }
        elsif ( $_ =~ /motion saved movie file.*?(\/.*$)/ ) {
                #print FILE "matched $_ , file = $1\n";
                $arg=undef;
                #@filelist=`find /var/www/webcam -type f -name \*\`date '+%Y%m%d'\`\*jpg -mtime 0|tail -5`;
                #@filelist=`ls -1rt /var/www/webcam/\`date '+%Y%m%d'\`\*jpg|tail -5`;
                @filelist=`ls -1rt /var/www/rcam/media/im\*\`date '+%Y%m%d'\`\*th.jpg|tail -5`;
                foreach(@filelist) { chomp $_; $arg .= "$_ "  }
                `/home/pi/scripts/mailattachment.py $arg` ;
        }
}
#close(FILE);


sub check {
        my $service = shift;
        open(CMD,"/usr/sbin/service $service status|");
        while(<CMD>) {
                if ( $_ =~ /failed/i ) {
                        system("/usr/sbin/service $service start");
                }
        }
        close(CMD);
}

#iptables service starter. /etc/inittab entry
#wp:2:respawn:/root/watch-pipe.pl < /root/my_pipe

