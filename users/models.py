from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("이메일은 필수입니다.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    LOGIN_TYPES = [
        ("normal", "일반"),
        ("kakao", "카카오"),
        ("naver", "네이버"),
        ("google", "구글"),
    ]
    email = models.EmailField(
        verbose_name="이메일",
        max_length=100,
        unique=True,
    )
    nickname = models.CharField("닉네임", max_length=20, unique=True)
    password = models.CharField("비밀번호", max_length=100)
    profile_image = models.ImageField("프로필 이미지", upload_to="profile_image", blank=True)
    login_type = models.CharField("로그인 타입", max_length=10, choices=LOGIN_TYPES, default="normal")
    following = models.ManyToManyField("self", verbose_name="팔로잉", symmetrical=False, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "password"]
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin
