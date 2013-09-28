from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, jid, password):
        user = self.model(
            email=self.normalize_email(email),
            jid=self.normalize_email(jid),
        )
        
        user.is_active=True
        
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, jid, password):
        user = self.model(
            email=self.normalize_email(email),
            jid=self.normalize_email(jid),
        )
        
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        
        user.set_password(password)
        user.save()
        return user     
