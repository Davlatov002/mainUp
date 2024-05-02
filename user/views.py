from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Profile, Transaction, Identified, MoneyOut, Strength
from drf_yasg.utils import swagger_auto_schema
from .serialazers import ProfileSerializer, ProfilesingupSerialazer, ProfileLoginserialazer, UpdateProfileSerializer, ProfileRefeleshSerialazer,VerificationCodeserialazer ,GMProfileserialazer, UpdatePasswordSerializer, Tranzaktionserialazer, UpdateEmPsSerializer,UserTranzaktionserialazer, MoneyOutserialazer, CreatMoneyOutserialazer, IdentifiedSerializer, StrengthSerialazer
import time, calendar
import random, string
from datetime import datetime, timedelta
from django.db.models import Sum, F
import json
from django.shortcuts import render, get_list_or_404, get_object_or_404

# gmail######
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

globals
code_lis = {}

def generate_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def send_email(subject, body, to_email):
    # Gmail pochtangiz va parolingizni kiriting
    gmail_user = 'netboxollc@gmail.com'
    gmail_password = "rfqdwyoszfrfoczl"

    # Xabar tayyorlash
    message = MIMEMultipart()
    message['From'] = gmail_user
    message['To'] = to_email
    message['Subject'] = subject

    # Xabarning matnini qo'shish
    message.attach(MIMEText(body, 'html'))

    # SMTP serveriga ulanish
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)

        # Xabarni yuborish
        server.sendmail(gmail_user, to_email, message.as_string())
#####


@swagger_auto_schema(method='PATCH', operation_description="Tiklamoqchi bo'lgan profilning ID sini kirting!")
@api_view(['PATCH'])
def send_otp(request, email):
    if request.method == 'PATCH':
        try:
            # Agar email bo'yicha profili topish mumkin bo'lsa
            profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            try:
                # Agar email bo'yicha topilmagan bo'lsa, username bo'yicha izlash
                profile = Profile.objects.get(username=email)
            except Profile.DoesNotExist:
                # Agar username bo'yicha ham topilmagan bo'lsa, xato qaytarish
                return Response({'message': -2 }, status=status.HTTP_400_BAD_REQUEST)
        six_digit_number = generate_random_string()
        gmail = str(profile.email)
        massag =f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .password-message {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                    border-radius: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="password-message">
                <p>Password Recovery - MinerUP</p>
                <p>Your new login password: <strong>{six_digit_number}</strong></p>
                <p>After that, you can only log in with this password.</p>
                <p>If this is not you, please contact us immediately.</p>
            </div>
        </body>
        </html>
    """
        send_email("Password",massag, gmail)
        profile.password = six_digit_number
        profile.save()
        return Response({'message': 1 },status=status.HTTP_200_OK)
    else:
        return Response({'message': -1 },status=status.HTTP_400_BAD_REQUEST)

# @swagger_auto_schema(method='PATCH', request_body=VerificationCodeserialazer, operation_description="Tiklamoqchi bo'lgan profilning ID sini kirting!")
# @api_view(['PATCH'])
# def confirmation_otp(request):
#     code = request.data.get("code")
#     if code in code_lis.keys():
#         del code_lis[code]
#         return Response({'message': 1 }, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': -2 },status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PATCH', operation_description="O'chirmoqchi bo'lgan Profileni ID sini kirting")
@api_view(['PATCH'])
def verify_email(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
    except:
        return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
    is_data = int(time.time())
    profile.is_verified = is_data
    profile.save()
    return Response({'message': 1}, status=status.HTTP_200_OK)


    







    
@swagger_auto_schema(method='POST', request_body=CreatMoneyOutserialazer, operation_description="Malumotlarni kirting")
@api_view(['POST'])
def moneyout(request, pk):
    stf = get_object_or_404(Strength, id = 1).money_out
    if stf == True:
        try:
            profile = Profile.objects.get(id=pk)
        except:
            return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)
        taim = int(time.time())
        wallet_address = request.data.get('wallet_addres')
        balance_netboo = request.data.get('balance_netbo')
        data = {"wallet_addres":wallet_address, "user":profile.id, "balance_netbo":balance_netboo, "created_at":taim}
        ser = MoneyOutserialazer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        profile.balance_netbo -= balance_netboo
        profile.save()
        return Response({'message': 1,"data":ser.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1,}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_moneyout_id(request, pk):
    moneyouts = MoneyOut.objects.filter(user=pk)
    serializer = MoneyOutserialazer(moneyouts, many=True)
    return Response({'message': 1, "data": serializer.data}, status=status.HTTP_200_OK)



@swagger_auto_schema(method='POST', request_body=IdentifiedSerializer, operation_description="Malumotlarni kirting")
@api_view(['POST'])
def upload_image(request, pk):
    serializer = IdentifiedSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    profile = Profile.objects.get(id=pk)
    profile.is_identified = None
    profile.save()
    serializer.save(user_id=pk)
    return Response({'message': 1, 'data': serializer.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_identified_id(request, pk):
    profile = Identified.objects.get(id=pk)
    serializer = IdentifiedSerializer(profile)
    return Response({'message': 1,"Identified":serializer.data}, status=status.HTTP_200_OK)



@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_tr_us(request, pk):
    profile = Profile.objects.get(id=pk).username
    tr = Transaction.objects.filter(username=profile)
    serialazer = UserTranzaktionserialazer(tr, many=True)
    return Response({'message': 1,"profile":serialazer.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_tr(request):
    tr = Transaction.objects.all()
    serializer = Tranzaktionserialazer(tr, many=True)
    return Response({'message': 1,"profile":serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def balance_history(request, pk):
    current_timestamp = int(time.time())
    current_date = datetime.utcfromtimestamp(current_timestamp).date()

    dey_sum = 0
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    moon_sum = [0] * days_in_month
    week_sum = [0] * 7
    profile = Profile.objects.get(id=pk)
    username_id = profile.id

    all_transactions = Transaction.objects.filter(user=username_id)

    # Kunlik tranzaksiyalar
    daily_transactions = all_transactions.filter(
        created_at__gte=current_timestamp - 86400,
        created_at__lt=current_timestamp
    )
    dey_sum = daily_transactions.aggregate(Sum('balance_netbo'))['balance_netbo__sum'] or 0

    # Haftalik tranzaksiyalar
    weekly_transactions = all_transactions.filter(
        created_at__gte=current_timestamp - (86400 * 7),
        created_at__lt=current_timestamp
    )
    week_sum = [0] * 7  # Reset week_sum
    for transaction in weekly_transactions:
        transaction_date = datetime.utcfromtimestamp(transaction.created_at).date()
        day_of_week = transaction_date.weekday()
        week_sum[day_of_week] += transaction.balance_netbo

    # Oylik tranzaksiyalar
    oylik_transactions = all_transactions.filter(
        created_at__gte=current_timestamp - (86400 * days_in_month),
        created_at__lt=current_timestamp
    )
    moon_sum = [0] * days_in_month  # Reset moon_sum
    for transaction in oylik_transactions:
        transaction_date = datetime.utcfromtimestamp(transaction.created_at).date()
        day_of_month = transaction_date.day - 1
        moon_sum[day_of_month] += transaction.balance_netbo

    return Response({'message': 1, 'daily': dey_sum, "weekly": week_sum, 'monthly': moon_sum}, status=status.HTTP_200_OK)
    


@swagger_auto_schema(method='PATCH', operation_description="O'chirmoqchi bo'lgan Profileni ID sini kirting")
@api_view(['PATCH'])
def archive_account(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    is_data = int(time.time())
    profile.is_archived = is_data
    profile.save()
    return Response({'message': 1}, status=status.HTTP_200_OK)



@swagger_auto_schema(method='PATCH', request_body=UpdatePasswordSerializer, operation_description="Parolni o'zgartirish uchun so'rov")
@api_view(['PATCH'])
def update_password(request, email):
    profile = get_object_or_404(Profile, email=email)
    serializer = UpdatePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    new_password = serializer.validated_data['password']
    profile.password = new_password
    profile.save()
    return Response({'message': 1 }, status=status.HTTP_200_OK)




@swagger_auto_schema(method='PATCH', operation_description="Ball berladigan profile ID sini kirting")
@api_view(['PATCH'])
def ad_reward(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
    except:
        return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)
    strength = Strength.objects.get(id = 1)
    username_id = profile.id
    taim2 = profile.last_mining
    taim1 = int(time.time())
    if taim2 + strength.taim <= taim1 :
        if profile.number_people < strength.number_people1:
            nom = strength.netbo + (strength.level1 * profile.number_people)
        elif profile.number_people < strength.number_people2:
            nom = strength.netbo + (strength.level2 * profile.number_people)
        else:
            nom = strength.netbo + (strength.level3 * profile.number_people)
        profile.balance_netbo += nom
        profile.save()
        data = {"user":username_id, 'balance_netbo':nom, "created_at":taim1}

        tran = Tranzaktionserialazer(data=data)
        profile.last_mining = int(time.time())
        profile.save()
        tran.is_valid(raise_exception=True)
        tran.save()
        return Response({'message': 1, "transaction":tran.data},status=status.HTTP_200_OK)
    else:
        return Response({'message': -2},status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='PATCH', request_body=ProfileRefeleshSerialazer, operation_description="Referal_link")
@api_view(['PATCH'])
def activate_referral_link(request, pk):    
    referal = request.data.get('referal_link')
    try:
        frend = Profile.objects.get(referal_link=referal)
    except:
        return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
    try:
        profile = Profile.objects.get(id=pk)
    except:
        return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
    if frend.is_identified == True:
        link = frend.referal_link
        profile.friend_referal_link = link
        profile.save()
        return Response({'message': 1}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -3}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='DELETE', operation_description="O'chirmoqchi bo'lgan Profileni ID sini kirting")
@api_view(['DELETE'])
def delete_profile(request, pk):
    praduct = get_object_or_404(Profile, id=pk)    
    praduct.delete()
    return Response({'message':1},status=status.HTTP_200_OK)


@swagger_auto_schema(method='PATCH', request_body=UpdateEmPsSerializer, operation_description="Yangilamaoqchi bo'lgan Profilening ID sini kirting")
@api_view(['PATCH'])
def update_email_password(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    data = UpdateEmPsSerializer(instance=profile, data=request.data)
    data.is_valid(raise_exception=True)
    new_email = data.validated_data.get('email')
    if Profile.objects.filter(email=new_email).exclude(id=pk).exists():
        return Response({'message': -4}, status=status.HTTP_400_BAD_REQUEST)
    data.save()
    profile.refresh_from_db()
    serializer = ProfileSerializer(profile)
    return Response({'message': 1, "profile": serializer.data}, status=status.HTTP_200_OK)
    

class UpdateProfileAPIView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    queryset = Profile.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_username = serializer.validated_data.get('username')
        if Profile.objects.filter(username=new_username).exclude(id=instance.id).exists():
            return Response({'message': -4}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        instance.refresh_from_db()
        return Response({'message': 1, "profile": ProfileSerializer(instance).data}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_profile_username(request, username):
    profile = get_object_or_404(Profile, username=username)
    serializer = ProfileSerializer(profile)
    return Response({'message': 1,"profile":serializer.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_profile_id(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    serializer = ProfileSerializer(profile)
    return Response({'message': 1,"profile":serializer.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_profile(request):
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    return Response({'message': 1,"profile":serializer.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', request_body=ProfileLoginserialazer, operation_description="Malumotlarni kirting")
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        profile = Profile.objects.get(username=username)
    except:
        return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)   
    if profile.password == password:
        profile_serializer = ProfileSerializer(profile)
        return Response({'message': 1, "profile":profile_serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)


    
@swagger_auto_schema(method='POST', request_body=ProfilesingupSerialazer, operation_description="Malumotlarni kirting")
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    # Profil ma'lumotlarini bir marta olish
    existing_profiles = Profile.objects.filter(username=username) | Profile.objects.filter(email=email)
    # Profil ma'lumotlarini tekshirish
    if existing_profiles.exists():
        return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ProfileSerializer(data=request.data)
    # Serializer ma'lumotlarini tekshirish
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 1, "profile": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_strength(request):
    strength = Strength.objects.get(id=1)
    serializer = StrengthSerialazer(strength)
    return Response({'message': 1,"strength":serializer.data}, status=status.HTTP_200_OK)