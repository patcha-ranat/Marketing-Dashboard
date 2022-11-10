CREATE TABLE IF NOT EXISTS posts (
    postID TEXT,
    postTime TEXT, -- need to be transformed to DATETIME later
    caption TEXT,
    reach INT,
    likesAndReactions INT,
    postClicks INT,
    comments INT,
    shares INT,
    PRIMARY KEY (postID)
);

CREATE TABLE IF NOT EXISTS campaigns (
    tagID TEXT,
    campaign TEXT,
    PRIMARY KEY (tagID)
);

CREATE TABLE IF NOT EXISTS postsAndTags (
    pk_postsAndTags TEXT,
    postID TEXT REFERENCES posts(postID),
    tagID TEXT REFERENCES campaigns(tagID),
    PRIMARY KEY (pk_postsAndTags)
);

INSERT INTO posts (postID, postTime, caption, reach, likesAndReactions, postClicks, comments, shares)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);

INSERT INTO campaigns (tagID, campaign)
VALUES (?, ?);

INSERT INTO postsAndTags (pk_postsAndTags, postID, tagID)
VALUES (?, ?, ?);