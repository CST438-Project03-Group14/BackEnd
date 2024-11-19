from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import User
from .serializers import UserSerializer
# import bcrypt
@api_view(['GET'])
def homePage(request):
    welcome = {'hi': 'welcome to the django api thingy. To see the response for any of these in json, put into the link the following \'format=json\' ',
              'links':['/newuser?username={username}&password={password}',
                       '/login?username={username}&password={password}',
                       '/logout?username={username}',
                       '/logout?username={username}&password={password}',
                       '/users',
                       '/users/delete?username={username}&user_id={user_id}',
                       '/users/update?username={username}&user_id={user_is}&new_username={new_username}&new_password={new_password}',
                       '/login/admin?username={username}&password={password}',
                        '/lists',
                        '/lists/list?list_id={list_id}',
                        '/lists/books?user_id={user_id}',
                        '/lists/addBook?user_id={user_id}&list_id={list_id}&book_id={book_id}',
                        '/lists/deleteBook?user_id={user_id}&list_id={list_id}&book_id={book_id}',
                        '/lists/add?user_id={user_id}&list_name={list_name}',
                        '/lists/delete?user_id={user_id}&list_id={list_id}',
                       ]}
    return Response(welcome)

# TODO: Make this admin only
@api_view(['GET'])
def getAllUsers(request):
    user_id = request.GET.get('user_id')

    if not (User.objects.filter(user_id=user_id).exists()):
        return Response({"error":"need admin perms"}, status=400)

    if (User.objects.get(user_id=user_id).is_admin == 0):
        return Response({"message":f"{user_id}","error":"need admin perms"}, status=400)

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
    # Check if a user with the same username already exists
    username = request.GET.get('username')
    password = request.GET.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    userObject = User.objects.create(username=username,password=password)
    serializer = UserSerializer(userObject)
    return Response(serializer.data, status=201)

@api_view(['PUT'])
def logIn(request):
    # Get the username and password from the request data
    username = request.GET.get('username')
    password = request.GET.get('password')
    
    # Check if the user with the given username exists
    try:
        user = User.objects.get(username=username)
        # Directly compare the passwords (for now until i figure out what Oauth needs)
        if password == user.password:
            user.signed_in = True
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "Invalid password"}, status=400)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

 
@api_view(['PUT'])
def adminLogIn(request):
    # Get the username and password from the request data
    username = request.GET.get('username')
    password = request.GET.get('password')

    # Check if the user with the given username exists and is admin
    try:
        user = User.objects.get(username=username)
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            #checking is user is an admin
            if(not user.is_admin):
               return Response({"error":"User is not admin"}, status=403)
            user.signed_in = True
            user.save()
            # Serialize and return the user data
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "Invalid password"}, status=400)
        
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(['PUT', 'DELETE'])
def logout_or_delete_account(request):
    username = request.GET.get('username')

    try:
        # Get the user by username
        user = User.objects.get(username=username)
        
        if request.method == 'PUT':
            # Logout user (signed_in = False)
            if user.signed_in:
                user.signed_in = False
                user.save()
                return Response({"message": f"{username} has successfully logged out.", "result" : True}, status=200)
            else:
                return Response({"error": f"{username} is not signed in.", "result" : False}, status=400)
        
        elif request.method == 'DELETE':
            # For DELETE, confirm password before deleting the account
            password = request.GET.get('password')
            
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                user.delete()
                return Response({"message": f"Account for {username} has been deleted." , "result" : True}, status=200)
            else:
                return Response({"error": "Password incorrect.", "result" : False}, status=400)
    
    except User.DoesNotExist:
        return Response({"error": "User not found", "result" : False}, status=404)

@api_view(['DELETE'])
def adminDeleteUser(request):
    username = request.GET.get('username')
    admin_id = request.GET.get('user_id')
    password = request.GET.get('password')

    #cheking that the user deleting an account is admin and exist
    try:
        admin = User.objects.get(user_id=admin_id)
        if(not admin.is_admin):
            return Response({"error":f"{admin.username} is not admin","result":False}, status=404)
    except User.DoesNotExist:
        return Response({"error": "Admin not found", "result":False}, status=404)

    try:
        user = User.objects.get(username=username)

        if bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
            user.delete()
            return Response({"message": f"Account of {username} has been deleted." , "result" : True}, status=200)
        else:
            return Response({"error": "Password incorrect.", "result" : False}, status=400)

    except User.DoesNotExist:
        return Response({"error": "User not found", "result":False}, status=404)

@api_view(['PUT'])
def updateUser(request):
    admin_id = request.GET.get('user_id')
    username = request.GET.get('username')
    new_username = request.GET.get('new_username')
    new_password = request.GET.get('new_password')
    password = request.GET.get('password')

    if admin_id:
        try:
            admin = User.objects.get(user_id=admin_id)
            admin_og_password = admin.password
            if not admin.is_admin:
                return Response({"error":f"{admin.username} is not admin","result":False}, status=404)
        except User.DoesNotExist:
            return Response({"error": "Admin not found", "result":False}, status=404)


    try:
        user = User.objects.get(username=username)
        og_password = user.password
    except User.DoesNotExist:
        return Response({"error":f"user {username} does not exist"}, status=404)
    
    try:
        user = User.objects.get(username=username)
        if new_username:
            if User.objects.filter(username=new_username).exists():
                return Response({"error": "Username already exists"}, status=400)
            user.username = new_username
        if new_password:
            user.password = new_password
        if admin_id:
            if bcrypt.checkpw(password.encode('utf-8'), admin_og_password.encode('utf-8')):
                user.save();
                return Response({"success": "User updated successfully"}, status=200)
            else:
                return Response({"error": "Wrong Password"}, status=401)
            
        if bcrypt.checkpw(password.encode('utf-8'), og_password.encode('utf-8')):

            user.save();
        else:
            return Response({"error": "Wrong Password"}, status=401)
        return Response({"success": "User updated successfully"}, status=200)
    except User.DoesNotExist:
        return Response({"error": f"user {username} does not exist"}, status=404)
