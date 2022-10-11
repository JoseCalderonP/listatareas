from dis import Instruction


instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS todo;',
    'DROP TABLE IF EXISTS users;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE users(
            id int primary key auto_increment,
            username varchar(50) unique not null,
            password varchar(255) not null
        )
    """,
    """
        CREATE TABLE todo(
                id int primary key auto_increment,
                created_by int not null,
                created_at timestamp not null default current_timestamp,
                description text not null,
                completed boolean not null,
                foreign key (created_by) references users(id)
            )
    """
]