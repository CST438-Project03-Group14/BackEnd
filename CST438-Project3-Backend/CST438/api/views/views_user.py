from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import User  # Updated import
from ..serializers import UserSerializer
# import bcrypt

#test

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Welcome to BookHive API',
        'endpoints': {
            'auth': {
                'login': '/api/login',
                'signup': '/api/newuser',
                'admin_login': '/api/login/admin',
                'logout': '/api/logout'
            },
            'books': {
                'list': '/api/books',
                'search': '/api/books/search',
                'manage': '/api/books/manage'
            },
            'lists': {
                'all': '/api/lists',
                'user': '/api/lists/user',
                'add': '/api/lists/add',
                'delete': '/api/lists/delete'
            }
        }
    })

@api_view(['GET'])
def getAllUsers(request):
    user_id = request.GET.get('user_id')
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


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
    logger.info(f"Attempting to create user with username: {request.GET.get('username')}")
    username = request.GET.get('username')
    password = request.GET.get('password')

    try:
        if User.objects.filter(username=username).exists():
            logger.warning(f"Username {username} already exists")
            return Response({"error": "Username already exists"}, status=400)

        userObject = User.objects.create(username=username, password=password)
        logger.info(f"Successfully created user: {username}")
        serializer = UserSerializer(userObject)
        return Response(serializer.data, status=201)
    except Exception as e:
        logger.error(f"Error creating user {username}: {str(e)}")
        return Response({"error": str(e)}, status=500)

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
