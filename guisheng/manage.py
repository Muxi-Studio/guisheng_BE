# coding: utf-8
"""
project management
 -- database management
    -- python manage.py db init: create migrations folder
    -- python manage.py db migrate: database migrate
    -- python manage.py db upgrate: upgrade database
    -- python manage.py shell
       >> Role.insert_roles() : create user roles

 -- add administrator
    -- python manage.py admin
       \_admin username:
       \_admin email:
       \_admin password:

 -- add users
    -- python manage.py adduser
       \_username:
       \_password:
       \_email:
       \_[1:moderator 2:admin 3:user]:

 -- run project
    -- python manage.py runserver

 -- shell environment
    -- python manage.py shell

 -- run your unit tests
    -- python manage.py test

"""

import sys
import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from guisheng_app import db, app
from guisheng_app.models import User, Role, News, Everydaypic, Article,Image,\
        Picture, Interaction, Comment, Like, Light, Collect,PostTag,Tag,Suggestion,Permission

# 编码设置
reload(sys)
sys.setdefaultencoding('utf-8')


manager = Manager(app)
migrate = Migrate(app, db)



def make_shell_context():
    """自动加载环境"""
    return dict(
        app = app,
        db = db,
        User = User,
        Role = Role,
        News = News,
        Everydaypic = Everydaypic,
        Article = Article,
        Picture = Picture,
        Interaction = Interaction,
        Comment = Comment,
        Collect = Collect,
        Like = Like,
        Light = Light,
        PostTag = PostTag,
        Tag = Tag,
        Suggestion = Suggestion,
        Image = Image
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """run your unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def admin():
    """add administrator"""
    from getpass import getpass
    username = raw_input("\_admin username: ")
    email = raw_input("\_admin email: ")
    password = getpass("\_admin password: ")
    u = User(
        email = email,
        name = username,
        password = password,
        role_id = 2
    )
    db.session.add(u)
    db.session.commit()
    print "<admin user %s add in database>" % username

@manager.command
def add_test_admin():
    """add test administrator"""
    from getpass import getpass
    username = "test1"
    email = "test1"
    password = "test1"
    u = User(
        email = email,
        name = username,
        password = password,
        role_id = 2
    )
    db.session.add(u)
    db.session.commit()
    print "<test admin user %s add in database>" % username

@manager.command
def adduser():
    """add user"""
    from getpass import getpass
    name = raw_input("\_username: ")
    email = raw_input("\_email: ")
    role_id = raw_input("\_[1:moderator 2:admin 3:user]: ")
    password = getpass("\_password: ")
    u = User(
        email = email,
        name = name,
        password = password,
        role_id = role_id
    )
    db.session.add(u)
    db.session.commit()
    print "<user %s add in database>" % name

@manager.command
def insert_roles():
    """
    insert all Roles in command line
    -------------------------------
    User: write & comment
    Moderator: write & comment & moderate_comments
    Administrator: full permissions
    """
    roles = {
        'User': (Permission.COMMENT,True),
        'Moderator': (Permission.COMMENT |
                      Permission.MODERATE_COMMENTS, False),
        'Administrator': (Permission.COMMENT | 
                          Permission.MODERATE_COMMENTS |
                          Permission.ADMINISTER, False)
    }
    for r in roles:
        role = Role.query.filter_by(name=r).first()
        if role is None:
            role = Role(name=r)
        role.permissions = roles[r][0]
        role.default = roles[r][1]
        db.session.add(role)
    db.session.commit()
    print 'roles has been inserted!'
    #return 'roles has been inserted!'


if __name__ == '__main__':
    manager.run()

