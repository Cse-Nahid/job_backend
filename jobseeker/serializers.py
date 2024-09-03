from rest_framework import serializers
from .models import Jobseeker

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]



class JobSeekerSerializer(serializers.ModelSerializer):
    # StringRelatedField for nested serializers, to only show the user name, not the whole user object data
    # user = serializers.StringRelatedField(many=False)

    # to view the user account details too
    user = UserSerializer(read_only=True)

    class Meta:
        model = Jobseeker
        fields = '__all__'

        read_only_fields = ["user", ]



# crating serializer for user registration
class JobSeekerRegistrationSerializer(serializers.ModelSerializer):
    fathers_name = serializers.CharField(max_length=20)
    mothers_name = serializers.CharField(max_length=20)
    address = serializers.CharField()
    contact_no = serializers.CharField(max_length=11, required=False)
    sex = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    age = serializers.IntegerField(validators=[MinValueValidator(18)])
    education = serializers.CharField()
    experience = serializers.CharField()
    confirm_password = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',  'fathers_name', 'mothers_name', 'address', 'contact_no', 'sex', 'age', 'education', 'experience', 'email', 'password', 'confirm_password'
        ]


    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        fathers_name = self.validated_data['fathers_name']
        mothers_name = self.validated_data['mothers_name']
        address = self.validated_data['address']

        sex = self.validated_data['sex']
        age = self.validated_data['age']
        education = self.validated_data['education']
        experience = self.validated_data['experience']

        contact_no = self.validated_data.get('contact_no')
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'error' : "Password Doesn't Matched."})
        
        if User.objects.filter(email = email, user_type = 'jobseeker').exists():
            raise serializers.ValidationError({'error' : "Email Already Exists."})
        
        account = User(
            username = username, first_name = first_name, last_name = last_name, email = email, 
            user_type = 'jobseeker',
        )
        print(account)
        account.set_password(password)

        account.is_active = False   # initially set to False, will be true after activation link validation

        account.save()


        jobseeker_account = Jobseeker(
            user = account,

            fathers_name = fathers_name, mothers_name = mothers_name, address = address, sex = sex, age = age, education = education, experience = experience, contact_no = contact_no
        )

        jobseeker_account.save()

        # returning the customUser account of jobseeker object model to use in the registrationViewSet
        return account
    