from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from App.database import db
from App.models.user import Review, Listing, User
from App.forms import ReviewForm
from datetime import datetime

review_bp = Blueprint('review', __name__, url_prefix='/reviews')

@review_bp.route('/listing/<int:listing_id>/create', methods=['GET', 'POST'])
@login_required
def create(listing_id):
    """Create a new review for an apartment (verified tenant only)"""
    # Ensure the user is a tenant
    if current_user.user_type != 'tenant':
        flash('Only tenants can submit reviews.', 'warning')
        return redirect(url_for('listing.detail', apartment_id=listing_id))
    
    # Verify tenant status
    if not current_user.is_verified:
        flash('Your tenant account needs to be verified before submitting reviews.', 'warning')
        return redirect(url_for('listing.detail', apartment_id=listing_id))
    
    # Get the listing
    listing = Listing.query.get_or_404(listing_id)
    
    # Check if the user has already reviewed this listing
    existing_review = Review.query.filter_by(
        user_id=current_user.id, 
        listing_id=listing_id
    ).first()
    
    if existing_review:
        flash('You have already reviewed this apartment.', 'warning')
        return redirect(url_for('listing.detail', apartment_id=listing_id))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            content=form.content.data,
            rating=form.rating.data,
            pros=form.pros.data,
            cons=form.cons.data,
            lease_period=form.lease_period.data,
            listing_id=listing_id,
            user_id=current_user.id
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('listing.detail', apartment_id=listing_id))
    
    return render_template('reviews/create.html', form=form, listing=listing, title='Write a Review')

@review_bp.route('/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(review_id):
    """Edit an existing review (author only)"""
    review = Review.query.get_or_404(review_id)
    
    # Check if the current user is the author
    if review.user_id != current_user.id:
        flash('You can only edit your own reviews.', 'danger')
        return redirect(url_for('listing.detail', apartment_id=review.listing_id))
    
    form = ReviewForm(obj=review)
    if form.validate_on_submit():
        review.content = form.content.data
        review.rating = form.rating.data
        review.pros = form.pros.data
        review.cons = form.cons.data
        review.lease_period = form.lease_period.data
        
        db.session.commit()
        
        flash('Review updated successfully!', 'success')
        return redirect(url_for('listing.detail', apartment_id=review.listing_id))
    
    return render_template('reviews/edit.html', form=form, review=review, title='Edit Review')

@review_bp.route('/<int:review_id>/delete', methods=['POST'])
@login_required
def delete(review_id):
    """Delete a review (author only)"""
    review = Review.query.get_or_404(review_id)
    
    # Check if the current user is the author
    if review.user_id != current_user.id:
        flash('You can only delete your own reviews.', 'danger')
        return redirect(url_for('listing.detail', apartment_id=review.listing_id))
    
    listing_id = review.listing_id
    
    db.session.delete(review)
    db.session.commit()
    
    flash('Review deleted successfully.', 'success')
    return redirect(url_for('listing.detail', apartment_id=listing_id))

@review_bp.route('/my-reviews')
@login_required
def my_reviews():
    """View reviews created by the current user (tenant only)"""
    if current_user.user_type != 'tenant':
        flash('Only tenants can have reviews.', 'warning')
        return redirect(url_for('index_views.index'))
    
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    return render_template('reviews/my_reviews.html', reviews=reviews, title='My Reviews')