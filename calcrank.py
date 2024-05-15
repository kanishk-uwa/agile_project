def update_ratings(winner, loser):
    # Set the rating change amounts
    rating_change = 25

    # Update ratings simply
    winner.elo_rating += rating_change
    loser.elo_rating -= rating_change


def assign_rank(user):
    if user.elo_rating >= 2000:
        return 'Gold'
    elif user.elo_rating >= 1500:
        return 'Silver'
    else:
        return 'Bronze'
