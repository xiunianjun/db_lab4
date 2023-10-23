/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2023/10/21 16:11:31                          */
/*==============================================================*/
use canteen_order;

-- drop trigger if exists Order_BEFORE_INSERT;

-- drop trigger if exists Order_AFTER_INSERT;

-- drop procedure if exists count_store_average_level;

-- alter table cmt 
--    drop foreign key FK_CMT_ORDER_COM_ORDERS;

-- alter table dish 
--    drop foreign key FK_DISH_STORE_PRD_STORE;

-- alter table dish_order 
--    drop foreign key FK_DISH_ORD_DISH_ORDE_ORDERS;

-- alter table dish_order 
--    drop foreign key FK_DISH_ORD_DISH_ORDE_DISH;

-- alter table orders 
--    drop foreign key FK_ORDERS_ORDER_USE_USERS;

-- alter table orders 
--    drop foreign key FK_ORDERS_STORE_ORD_STORE;

-- alter table store 
--    drop foreign key FK_STORE_CANTEEN_S_CANTEEN;

-- drop 
-- table if exists canteen_store_dishes_info;

-- drop index Index_user_name on users;

/*==============================================================*/
/* Table: admin                                                 */
/*==============================================================*/
create table admin
(
   admin_id             int not null  comment '',
   admin_name           varchar(16) not null  comment '',
   admin_psw            varchar(256) not null  comment '',
   primary key (admin_id)
);

/*==============================================================*/
/* Table: canteen                                               */
/*==============================================================*/
create table canteen
(
   canteen_id           int not null  comment '',
   canteen_name         varchar(16) not null  comment '',
   canteen_status       bool  comment '',
   primary key (canteen_id)
);

/*==============================================================*/
/* Table: cmt                                                   */
/*==============================================================*/
create table cmt
(
   comment_id           int not null  comment '',
   order_id             int not null  comment '',
   comment_content      varchar(512)  comment '',
   comment_level        int not null  comment '',
   comment_time         timestamp not null  comment '',
   primary key (comment_id)
);

/*==============================================================*/
/* Table: dish                                                  */
/*==============================================================*/
create table dish
(
   dish_id              int not null  comment '',
   dish_name            varchar(16) not null  comment '',
   dish_intro           varchar(128)  comment '',
   dish_price           numeric(4,1) not null  comment '',
   store_id             int not null  comment '',
   dish_sales           int not null  comment '',
   dish_store           int not null  comment '',
   primary key (dish_id)
);

/*==============================================================*/
/* Table: dish_order                                            */
/*==============================================================*/
create table dish_order
(
   order_id             int not null  comment '',
   dish_id              int not null  comment '',
   primary key (order_id, dish_id)
);

/*==============================================================*/
/* Table: orders                                                */
/*==============================================================*/
create table orders
(
   order_id             int not null  comment '',
   user_id              int not null  comment '',
   store_id             int not null  comment '',
   total                decimal(4,1) not null  comment '',
   create_time          timestamp not null  comment '',
   dish_list            varchar(1024) not null  comment '',
   primary key (order_id)
);

/*==============================================================*/
/* Table: store                                                 */
/*==============================================================*/
create table store
(
   store_id             int not null  comment '',
   store_name           varchar(16) not null  comment '',
   canteen_id           int not null  comment '',
   primary key (store_id)
);

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users
(
   user_id              int not null  comment '',
   user_name            varchar(16) not null  comment '',
   user_psw             varchar(256) not null  comment '',
   user_balance         int not null  comment '',
   user_status          bool not null  comment '',
   primary key (user_id)
);

/*==============================================================*/
/* Index: Index_user_name                                       */
/*==============================================================*/
create unique index Index_user_name on users
(
   user_name
);

/*==============================================================*/
/* Table: vendor                                                */
/*==============================================================*/
create table vendor
(
   vendor_id            int not null  comment '',
   store_id             int not null  comment '',
   vendor_name          varchar(16) not null  comment '',
   vendor_psw           varchar(256) not null  comment '',
   vendor_status        bool not null  comment '',
   primary key (vendor_id)
);

/*==============================================================*/
/* View: canteen_store_dishes_info                              */
/*==============================================================*/
create VIEW  canteen_store_dishes_info
 as
select `canteen`.`canteen_id` AS `canteen_id`,
        `store`.`store_id` AS `store_id`,
        `store`.`store_name` AS `store_name`,
        `dish`.`dish_name` AS `dish_name`,
        `dish`.`dish_intro` AS `dish_intro`,
        `dish`.`dish_price` AS `dish_price` ,
        `dish`.`dish_sales` AS `dish_sales`
from dish, store, canteen 
where ((`dish`.`store_id` = `store`.`store_id`) 
        and (`store`.`canteen_id` = `canteen`.`canteen_id`)) 
order by `canteen`.`canteen_id` desc;

alter table cmt add constraint FK_CMT_ORDER_COM_ORDERS foreign key (order_id)
      references orders (order_id) on delete restrict on update restrict;

alter table dish add constraint FK_DISH_STORE_PRD_STORE foreign key (store_id)
      references store (store_id) on delete restrict on update restrict;

alter table dish_order add constraint FK_DISH_ORD_DISH_ORDE_ORDERS foreign key (order_id)
      references orders (order_id) on delete restrict on update restrict;

alter table dish_order add constraint FK_DISH_ORD_DISH_ORDE_DISH foreign key (dish_id)
      references dish (dish_id) on delete restrict on update restrict;

alter table orders add constraint FK_ORDERS_ORDER_USE_USERS foreign key (user_id)
      references users (user_id) on delete restrict on update restrict;

alter table orders add constraint FK_ORDERS_STORE_ORD_STORE foreign key (store_id)
      references store (store_id) on delete restrict on update restrict;

alter table store add constraint FK_STORE_CANTEEN_S_CANTEEN foreign key (canteen_id)
      references canteen (canteen_id) on delete restrict on update restrict;


DELIMITER //

-- DROP PROCEDURE IF EXISTS count_store_average_level;

CREATE PROCEDURE count_store_average_level(IN storeId INT)
BEGIN
    DECLARE totalRating INT;
    DECLARE totalOrders INT;
    DECLARE averageRating DECIMAL(3, 2);

    -- 创建一个临时表来存储计算结果
    CREATE TEMPORARY TABLE temp_average_rating (
        store_id INT,
        average_rating DECIMAL(3, 2)
    );

    -- 计算总评分和订单数
    SELECT SUM(comment_level), COUNT(*) INTO totalRating, totalOrders
    FROM cmt
    WHERE order_id IN (SELECT order_id FROM orders WHERE store_id = storeId);

    -- 避免除以零错误
    IF totalOrders > 0 THEN
        -- 计算平均评分
        SET averageRating = totalRating / totalOrders;

        -- 将结果插入临时表
        INSERT INTO temp_average_rating (store_id, average_rating) VALUES (storeId, averageRating);
    END IF;

    -- 输出结果
    SELECT * FROM temp_average_rating;
    
    -- 删除临时表
    DROP TEMPORARY TABLE IF EXISTS temp_average_rating;
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER Order_BEFORE_INSERT
BEFORE INSERT ON orders
FOR EACH ROW
SET NEW.create_time = CURRENT_TIMESTAMP;


-- 创建一个 AFTER INSERT 触发器
CREATE TRIGGER Order_AFTER_INSERT
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE tmp_dish_name VARCHAR(255);
    DECLARE start_pos INT DEFAULT 1;
    DECLARE end_pos INT;

    -- 处理订单中的每个菜品
    WHILE start_pos <= LENGTH(NEW.dish_list) DO
        SET end_pos = IFNULL(NULLIF(LOCATE(';', NEW.dish_list, start_pos), 0), LENGTH(NEW.dish_list) + 1);
        SET tmp_dish_name = TRIM(SUBSTRING(NEW.dish_list, start_pos, end_pos - start_pos));

        -- 更新菜品库存和销量
        UPDATE dish SET dish_store = dish_store - 1, dish_sales = dish_sales + 1 WHERE dish_name = tmp_dish_name;

        SET start_pos = end_pos + 1;
    END WHILE;
END // 
DELIMITER ;
