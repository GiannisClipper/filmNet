## FilmNet

This is a demo site, designed and written for practicing web development with python's Django. UI/UX written in plain HTML/CSS, data storage based on SQL database while images saved in file system as files and email sending powered by smtp.gmail.com.

It works like __a forum consisted of users, film posts and comments__ on films. Data are visible to all site visitors but only registered users can post new films and comments as well as modify or delete their own posts.

Users management is a customization of Django's built-in authentication system. Beyond username and password, an email address is required when signing up and used for account confirmation and activation.

Although the site follows the recommented security rules (ex. stores hashes instead of actual passwords), __you are advised not to use same passwords like email or bank accounts and not expose other crucial personal data__ (remember is just a demo site).

A film post requires a title which optionally accompanied by a year, a summary and an image (uploaded either from a local file or from a url on the Internet). A comment post requires a comment text. Both film and comment posts store the user-owner and dates-times when created and last updated.

Films or comments lists ordered from most recent to less recent (created or updated) using pagination (10 records per page). Within their corresponded film, comments printed in order they 've been created all in the same page.

Hope to enjoy your tour in site.

Live demo here https://giannisclipper.pythonanywhere.com/

_Athens 25 Mar 2019, Giannis Clipper_