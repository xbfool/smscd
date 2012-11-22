__author__ = 'xbfool'

import cherrypy
import db.db
import handler.handle_auth

class Smsd4:
    def __init__(self):
        self.db = db.db.create_db()

    @cherrypy.expose
    def auth(self, type='plain', rettype='json', *args, **kargs):
        print args
        print kargs
        ret =  handler.handle_auth.handle_auth(self, kargs)
        return ret
    @cherrypy.expose
    def echo(self):
        return 'echo'

    @cherrypy.expose
    def changepwd(self):
        return 'changepwd'

    @cherrypy.expose
    def add_user(self):
        return 'adduser'

    @cherrypy.expose
    def addmessage(self):
        return 'addmessage'

    @cherrypy.expose
    def sendmessagelist(self):
        return 'sendmessagelist'

    @cherrypy.expose
    def sendmessage(self):
        return 'sendmessage'

    @cherrypy.expose
    def userinfo(self):
        return 'userinfo'

    @cherrypy.expose
    def listchildren(self):
        return 'listchildren'

    @cherrypy.expose
    def listmsg(self):
        return 'listmsg'

    @cherrypy.expose
    def listcheckmsg(self):
        return 'listcheckmsg'

    @cherrypy.expose
    def msginfo(self):
        return 'msginfo'

    @cherrypy.expose
    def setuserstatus(self):
        return 'setuserstatus'

    @cherrypy.expose
    def manageuser(self):
        return 'manageuser'

    @cherrypy.expose
    def deleteuserlist(self):
        return 'deleteuserlist'

    @cherrypy.expose
    def deleteuser(self):
        return 'deleteuser'

    @cherrypy.expose
    def managemsg(self):
        return 'managemsg'


    @cherrypy.expose
    def queryreport(self):
        return 'queryreport'

    @cherrypy.expose
    def uploadreport(self):
        return 'uploadreport'

    @cherrypy.expose
    def channelqueryreport(self):
        return 'channelqueryreport'

    @cherrypy.expose
    def addmsglog(self):
        return 'addmsglog'

    @cherrypy.expose
    def listlog(self):
        return 'listlog'

    @cherrypy.expose
    def getphonebookinfo(self):
        return 'getphonebookinfo'

    @cherrypy.expose
    def addphonebook(self):
        return 'addphonebook'

    @cherrypy.expose
    def managephonebook(self):
        return 'managephonebook'

    @cherrypy.expose
    def deletephonebook(self):
        return 'deletephonebook'

    @cherrypy.expose
    def getaddresslistinfo(self):
        return 'getaddresslistinfo'

    @cherrypy.expose
    def addaddresslist(self):
        return 'addaddresslist'

    @cherrypy.expose
    def deleteaddresslist(self):
        return 'deleteaddresslist'

    @cherrypy.expose
    def getphonelistdata(self):
        return 'getphonelistdata'

    @cherrypy.expose
    def getallphoneinfo(self):
        return 'getallphoneinfo'

    @cherrypy.expose
    def addphone(self):
        return 'addphone'

    @cherrypy.expose
    def managephone(self):
        return 'managephone'

    @cherrypy.expose
    def deletephonelist(self):
        return 'deletephonelist'

    @cherrypy.expose
    def addphonelist(self):
        return 'addphonelist'

    @cherrypy.expose
    def change_user_msg_postfix(self):
        return 'change_user_msg_postfix'
cherrypy.quickstart(Smsd4())