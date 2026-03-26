document.addEventListener('DOMContentLoaded', function () {
    const reviewForm = document.getElementById('review-form');
    const commentForm = document.getElementById('comment-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(reviewForm);

            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert(data.error || 'Could not submit review.');
                    return;
                }

                const noReviewsText = document.getElementById('no-reviews-text');
                if (noReviewsText) {
                    noReviewsText.remove();
                }

                const reviewsList = document.getElementById('recent-reviews-list');

                const newReview = document.createElement('div');
                newReview.className = 'recent-review-item';
                newReview.innerHTML = `
                    <div class="recent-review-user">
                        <span class="recent-review-icon">◯</span>
                        <div>
                            <strong>${data.username}</strong>
                            <p>${data.comment}</p>
                        </div>
                    </div>
                    <span class="recent-review-score">${data.rating} ★</span>
                `;

                reviewsList.prepend(newReview);

                const summaryBox = document.getElementById('rating-summary-box');
                summaryBox.innerHTML = `
                    <h3>Rated ${data.average_rating} ★</h3>
                    <p>Based on ${data.review_count} Review${data.review_count == 1 ? '' : 's'}</p>
                `;

                reviewForm.outerHTML = '<p class="already-reviewed-text">You have already reviewed this destination.</p>';
            })
            .catch(error => {
                console.error('Review submission failed:', error);
            });
        });
    }

    if (commentForm) {
        commentForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(commentForm);

            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert(data.error || 'Could not submit comment.');
                    return;
                }

                const noCommentsText = document.getElementById('no-comments-text');
                if (noCommentsText) {
                    noCommentsText.remove();
                }

                const commentsBox = document.getElementById('comments-box');

                const newComment = document.createElement('div');
                newComment.className = 'comment-card';
                newComment.innerHTML = `
                    <div class="comment-top">
                        <span class="comment-user">
                            <span class="comment-user-icon">◯</span>
                            <strong>${data.username}</strong>
                        </span>
                        <span class="comment-date">${data.created_at}</span>
                    </div>
                    <p>${data.text}</p>
                `;

                commentsBox.prepend(newComment);

                const commentsHeading = document.getElementById('comments-heading');
                commentsHeading.textContent = `Comments (${data.comment_count})`;

                commentForm.reset();
            })
            .catch(error => {
                console.error('Comment submission failed:', error);
            });
        });
    }
});