def update_ratings(winner, loser):
    # Set the rating change amounts
    rating_change = 25

    # Update ratings simply
    winner.elo_rating += rating_change
    loser.elo_rating -= rating_change
