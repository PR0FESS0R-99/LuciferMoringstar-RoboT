
import random
import logging

async def save_poster(imdb_id, title, year, url):
    try:
        data = Poster(
            imdb_id=imdb_id,
            title=title,
            year=int(year),
            poster=url
        )
    except ValidationError:
        logger.exception('Error occurred while saving poster in database')
    else:
        try:
            await data.commit()
        except DuplicateKeyError:
            logger.warning("already saved in database")
        else:
            logger.info("Poster is saved in database")
