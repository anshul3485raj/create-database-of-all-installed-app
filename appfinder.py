import winreg
import sqlite3
con=sqlite3.Connection("apps")
cur=con.cursor()
#coded  anshul raj (github-anshul3485raj) pls follow on github
cur.execute("create table if not exists inistalledapp(app_name varchar(40) ,app_location varchar(56) )")
def app(hive, flag):
    reg = winreg.ConnectRegistry(None, hive)
    key = winreg.OpenKey(reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    skey = winreg.QueryInfoKey(key)[0]

    applist = []

    for i in range(skey):
        app = {}
        try:
            skeyname = winreg.EnumKey(key, i)
            askey = winreg.OpenKey(key, skeyname)
            app['name'] = winreg.QueryValueEx(askey, "DisplayName")[0]
            app['i']=winreg.QueryValueEx(askey,"InstallLocation")[0]


            applist.append(app)
        except EnvironmentError:
            continue

    return applist

applist = app(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + app(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + app(winreg.HKEY_CURRENT_USER,0)

for app in applist:
    r=[app['name'],"-",app['i']]
    a=(r[0],r[2])
    print(a)
    cur.execute("insert OR IGNORE into inistalledapp values(?,?)", a)
    con.commit()

print('Number of installed apps: %s' % len(applist))


