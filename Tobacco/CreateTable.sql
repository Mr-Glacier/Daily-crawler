CREATE TABLE
IF
	NOT EXISTS tobacco_brand (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	source_id TEXT,
	brand_type TEXT,
	brand_name TEXT,
	brand_url TEXT,
	down_state TEXT,
	down_time TEXT
	);

CREATE TABLE
IF
	NOT EXISTS tobacco_brand_details (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	source_id TEXT,
	brand_title TEXT,
	brand_pinyin TEXT,
	brand_introduce TEXT,
	brand_image_url TEXT,
	page_number INTEGER,
	down_state TEXT,
	down_time TEXT
	);


	CREATE TABLE
IF
	NOT EXISTS tobacco_specifications (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		brand_source_id TEXT,
		specifications_source_id TEXT,
		specifications_name TEXT,
		specifications_url TEXT,
		specifications_pic_url TEXT,
		specifications_norm TEXT,
		specifications_xh_number TEXT,
		specifications_th_number TEXT,
		specifications_price TEXT,
		down_state TEXT,
		down_time TEXT
	);
CREATE TABLE
IF
	NOT EXISTS tobacco_specifications_details (
	  id INTEGER PRIMARY KEY AUTOINCREMENT,
		specifications_source_id TEXT,
		specifications_title TEXT,
		specifications_small TEXT,
		specifications_product_type TEXT,
		specifications_product_tar_amount TEXT,
		specifications_product_nicotine_content TEXT,
		specifications_product_carbon_monoxide TEXT,
		specifications_product_th_size TEXT,
		specifications_product_packaging TEXT,
		specifications_product_cigarette_norm TEXT,
		specifications_product_cigarette_length TEXT,
		specifications_product_xh_number TEXT,
		specifications_product_th_number TEXT,
		specifications_product_xh_price TEXT,
		specifications_product_th_price TEXT,
		specifications_product_wholesale_price TEXT,
		specifications_product_availability TEXT
		);