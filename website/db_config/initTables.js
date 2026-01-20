const pool = require("../services/db");
//tables are dropped to ensure that the tables are cleared before we create them again

const SQLSTATEMENT = `
DROP TABLE IF EXISTS Reviews;

DROP TABLE IF EXISTS UserStage;

DROP TABLE IF EXISTS Report;

DROP TABLE IF EXISTS Vulnerability;

DROP TABLE IF EXISTS Stage;

DROP TABLE IF EXISTS User;

CREATE TABLE User ( 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    username TEXT NOT NULL, 
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    reputation INT DEFAULT 0,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 
CREATE TABLE Vulnerability ( 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    type TEXT NOT NULL, 
    description TEXT NOT NULL, 
    points INT NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 
CREATE TABLE Report ( 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    user_id INT NOT NULL, 
    vulnerability_id INT NOT NULL, 
    status BOOLEAN NOT NULL DEFAULT 0,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 ); 

CREATE TABLE Stage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    required_potions INT NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE UserStage (
    user_id INT NOT NULL,
    stage_id INT NOT NULL,
    cleared_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, stage_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (stage_id) REFERENCES Stage(id)
);

CREATE TABLE Reviews (
  id INT PRIMARY KEY AUTO_INCREMENT,
  review_amt INT NOT NULL,
  review_text TEXT,
  user_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES User(id)
);

SELECT 
  Report.user_id, 
  Report.vulnerability_id, 
  User.reputation AS user_reputation
FROM Report
INNER JOIN Vulnerability ON Report.vulnerability_id = Vulnerability.id
INNER JOIN User ON Report.user_id = User.id;

SELECT 
  User.username, 
  Stage.name
FROM UserStage
INNER JOIN User ON UserStage.user_id = User.id
INNER JOIN Stage ON UserStage.stage_id = Stage.id;

SELECT 
  Reviews.id, Reviews.review_amt, Reviews.review_text, Reviews.created_at,
  User.username
FROM Reviews
INNER JOIN User ON Reviews.user_id = User.id;

INSERT INTO Stage (name, description, required_potions) VALUES
  ('Cake Monster Area', 'Cake monsters dancing in chaos.', 100),
  ('Juicy Bat Swarm', 'Bats that feast on juicy fruits.', 300),
  ('Shadow Slime Blockade', 'An oozing menace blocks your path.', 400),
  ('Carnivorous Rose Garden', 'Don’t get charmed by the roses.', 700),
  ('Sun vs Moon Duel Area', 'Balance day and night in one fight.', 1400);

`;

pool.query(SQLSTATEMENT, (error, results, fields) => {
  if (error) {
    console.error("Error creating tables:", error);
  } else {
    console.log("Tables created successfully:", results);
  }
  process.exit();
});
