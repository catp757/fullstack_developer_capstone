from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create a `login_user` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_user` view to handle sign out request
def logout_user(request):
    logout(request)  # Terminate user session
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)

# Create a `register_user` view to handle sign up request
@csrf_exempt
def register_user(request):

    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except BaseException:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if (count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name,
                     "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})

# Update the `get_dealerships` render list of dealerships all by default,
# particular state if state is passed
def get_dealerships(request, state="All"):
    if (state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        logger.info(f"GETTING DEALER REVIEWS - /fetchReviews/dealer/{dealer_id}")
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        if not reviews:
            logger.warning(f"No reviews found for dealer ID {dealer_id}")
            return JsonResponse({"status": 200, "reviews": []})

        processed_reviews = []
        for review_detail in reviews:
            try:
                sentiment_response = analyze_review_sentiments(review_detail.get('review', ''))
                sentiment = sentiment_response.get('sentiment', 'neutral')
                review_detail['sentiment'] = sentiment
            except Exception as e:
                logger.error(f"Sentiment analysis failed for review: {review_detail}. Error: {e}")
                review_detail['sentiment'] = "neutral"
            
            processed_reviews.append(review_detail)

        return JsonResponse({"status": 200, "reviews": processed_reviews})

    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})
        

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if (dealer_id):
        logger.error("GETTING DEALER DETAILS - /fetchDealer/")
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            success = post_review(data)
            if success:
                return JsonResponse({"status": 200})
            else:
                return JsonResponse({"status": 500, "message": "Review failed to post"})
        except Exception as e:
            print("Exception in add_review:", e)
            return JsonResponse({"status": 500, "message": "Server error"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
