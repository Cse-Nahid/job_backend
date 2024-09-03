from rest_framework import serializers
from .models import Employer

from django.contrib.auth import get_user_model

User = get_user_model()




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type']



class EmployerSerializer(serializers.ModelSerializer):
    # StringRelatedField for nested serializers, to only show the user name, not the whole user object data
    # user = serializers.StringRelatedField(many=False)

    # to view the user account details too
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employer
        fields = '__all__'




# crating serializer for user registration
class EmployerRegistrationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(max_length=50)
    company_address = serializers.CharField()
    business_info = serializers.CharField()
    
    confirm_password = serializers.CharField(max_length=20, required=True)


    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'company_name', 'company_address', 'business_info', 'email', 'password', 'confirm_password'
        ]


    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        company_name = self.validated_data['company_name']
        company_address = self.validated_data['company_address']
        business_info = self.validated_data['business_info']

        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'error' : "Password Doesn't Matched."})
        
        if User.objects.filter(email = email, user_type = 'employer').exists():
            raise serializers.ValidationError({'error' : "Email Already Exists."})
        
        account = User(
            username = username, first_name = first_name, last_name = last_name, email = email, 
            user_type = 'employer',
        )
        print(account)
        account.set_password(password)

        account.is_active = False   # initially set to False, will be true after activation link validation

        account.save()


        employer_account = Employer(
            user = account,

            company_name = company_name, company_address = company_address, business_info = business_info
        )

        employer_account.save()

        # returning the customUser account of employer_account object model to use in the registrationViewSet
        return account
    