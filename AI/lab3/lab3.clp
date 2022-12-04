
(deftemplate cpu_struct "CPU struct"
  (slot name (type STRING))
  (slot work (type STRING) (allowed-values "min" "doc" "max" "server"))
  (slot W (type STRING) (allowed-values "low" "high"))
  (slot price (type STRING) (allowed-values "low" "high"))
  (slot size (type STRING) (allowed-values "small" "standard"))
);


(deffacts initial
  (cpu_struct (name "allwinner H5 cortex-A53") (work "min") (W "low") (price "low") (size "small"));
  (cpu_struct (name "Z-01") (work "min") (W "low") (price "high") (size "small"));
  (cpu_struct (name "sempron M140") (work "min") (W "high") (price "low") (size "small"));
  ;(cpu_struct (name "") (work "min") (W "high") (price "high") (size "small"));
  (cpu_struct (name "celeron j1800") (work "min") (W "low") (price "low") (size "standard"));
  ;(cpu_struct (name "") (work "min") (W "low") (price "high") (size "standard"));
  (cpu_struct (name "celeron 440") (work "min") (W "high") (price "low") (size "standard"));
  (cpu_struct (name "celeron 400") (work "min") (W "high") (price "high") (size "standard"));


  (cpu_struct (name "core 2 Duo E8500") (work "doc") (W "high") (price "low") (size "standard"));
  (cpu_struct (name "e2-3800") (work "doc") (W "low") (price "low") (size "standard"));
  (cpu_struct (name "Pentium 4 3.0") (work "doc") (W "high") (price "high") (size "standard"));
  ;(cpu_struct (name "") (work "doc") (W "low") (price "high") (size "standard"));
  (cpu_struct (name "celeron 847") (work "doc") (W "low") (price "low") (size "small"));
  (cpu_struct (name "i5-4300U") (work "doc") (W "high") (price "high") (size "small"));
  (cpu_struct (name "pentium Gold 5405U") (work "doc") (W "low") (price "high") (size "small"));
  (cpu_struct (name "i3-2350M") (work "doc") (W "high") (price "low") (size "small"));

  
  (cpu_struct (name "i5-3570") (work "max") (W "high") (price "low") (size "standard"));
  (cpu_struct (name "i5-9400F") (work "max") (W "high") (price "high") (size "standard"));
  ;(cpu_struct (name "") (work "max") (W "low") (price "low") (size "standard"));
  ;(cpu_struct (name "") (work "max") (W "low") (price "high") (size "standard"));
  ;(cpu_struct (name "") (work "max") (W "high") (price "low") (size "small"));
  (cpu_struct (name "i9-8950HK") (work "max") (W "high") (price "high") (size "small"));
  (cpu_struct (name "Broadcom BCM2711 ARM Cortex-A72") (work "max") (W "low") (price "low") (size "small"));
  (cpu_struct (name "Apple M1") (work "max") (W "low") (price "high") (size "small"));


  (cpu_struct (name "neoverse E1") (work "server") (W "low") (price "low") (size "small"));
  (cpu_struct (name "atom C2518") (work "server") (W "low") (price "high") (size "small"));
  (cpu_struct (name "pentium D-1507") (work "server") (W "high") (price "low") (size "small"));
  (cpu_struct (name "atom c2758") (work "server") (W "high") (price "high") (size "small"));
  ;(cpu_struct (name "") (work "server") (W "low") (price "low") (size "standard"));
  (cpu_struct (name "xeon E3-1105C") (work "server") (W "low") (price "high") (size "standard"));
  (cpu_struct (name "xeon E5-2640") (work "server") (W "high") (price "low") (size "standard"));
  (cpu_struct (name "epyc 7351P") (work "server") (W "high") (price "high") (size "standard"));
);

(defrule data-input
(initial-fact)
=>
(assert (user_want 0));
);

(defrule R_circle_start
(user_want 0)
?f_addr <- (user_want 0)
=>
(printout t crlf "Please enter 1 if you want take recommendation" crlf
                              "or 2 if you want to add new processor" crlf
                              "or 3 if you want to exit" crlf "> ");
(bind ?user_want (read));
(assert (user_want ?user_want));
(retract ?f_addr);
);

(defrule R_bye
(user_want 3)
=>
(printout t crlf "Bye! " crlf);
);

(defrule R_if1_2
(user_want 2)
=>
(printout t crlf "Enter processor name: " crlf "> ");
(bind ?buff1 (str-cat (read)));
(assert (new_proc_name ?buff1));

(printout t crlf "Enter processor price (rub): " crlf "> ");
(bind ?buff2 (read));
(assert (new_proc_price_rub ?buff2));

(printout t crlf "Enter processor target (min, doc, max or server): " crlf "> ");
(bind ?buff3 (str-cat (read)));
(assert (new_proc_work ?buff3));

(printout t crlf "Enter processor TDP (watt): " crlf "> ");
(bind ?buff4 (read));
(assert (new_proc_W_W ?buff4));

(printout t crlf "Enter processor socket (small or standard): " crlf "> ");
(bind ?buff5 (str-cat (read)));
(assert (new_proc_size ?buff5));
);

(defrule R_if2_1
(user_want 2)
(new_proc_price_rub ?x)
(test (< ?x 15000))
?f_addr <- (new_proc_price_rub ?x)
=>
(assert (new_proc_price "low"));
(retract ?f_addr);
);

(defrule R_if2_2
(user_want 2)
(new_proc_price_rub ?x)
(test (>= ?x 15000))
?f_addr <- (new_proc_price_rub ?x)
=>
(assert (new_proc_price "high"));
(retract ?f_addr);
);

(defrule R_if3_1
(user_want 2)
(new_proc_W_W ?x)
(test (< ?x 40))
?f_addr <- (new_proc_W_W ?x)
=>
(assert (new_proc_W "low"));
(retract ?f_addr);
);

(defrule R_if3_2
(user_want 2)
(new_proc_W_W ?x)
(test (>= ?x 40))
?f_addr <- (new_proc_W_W ?x)
=>
(assert (new_proc_W "high"));
(retract ?f_addr);
);

(defrule R_new_proc
(user_want 2)
(new_proc_name ?x_name)
(new_proc_price ?x_price)
(new_proc_work ?x_work)
(new_proc_W ?x_W)
(new_proc_size ?x_size)
?f_addr_0 <- (user_want 2)
?f_addr_1 <- (new_proc_name ?x_name)
?f_addr_2 <- (new_proc_price ?x_price)
?f_addr_3 <- (new_proc_work ?x_work)
?f_addr_4 <- (new_proc_W ?x_W)
?f_addr_5 <- (new_proc_size ?x_size)
=>
(assert (cpu_struct (name ?x_name) (work ?x_work) (W ?x_W) (price ?x_price) (size ?x_size)));
(retract ?f_addr_1 ?f_addr_2 ?f_addr_3 ?f_addr_4 ?f_addr_5 ?f_addr_0);
(assert (user_want 0));
);



(defrule R_if1_1
(user_want 1)
=>

(printout t crlf "Enter needed processor price (low or high): " crlf "> ");
(bind ?buff2 (str-cat (read)));
(assert (user_proc_price ?buff2));

(printout t crlf "Enter processor target (min, doc, max or server): " crlf "> ");
(bind ?buff3 (str-cat (read)));
(assert (user_proc_work ?buff3));

(printout t crlf "Enter needed processor energy use (low or high): " crlf "> ");
(bind ?buff4 (str-cat (read)));
(assert (user_proc_W ?buff4));

(printout t crlf "Enter needed processor socket (small or standard): " crlf "> ");
(bind ?buff5 (str-cat (read)));
(assert (user_proc_size ?buff5));
);

(defrule R_predict
(user_want 1)
(user_proc_price ?x_price)
(user_proc_work ?x_work)
(user_proc_W ?x_W)
(user_proc_size ?x_size)
(cpu_struct (name ?x_name) (work ?x_work) (W ?x_W) (price ?x_price) (size ?x_size))
?f_addr <- (user_want 1)
=>
(printout t crlf "Founded cpu for you: " ?x_name ". " crlf);
(retract ?f_addr);
(assert (user_want 0));
);

(defrule R_predict_not
(user_want 1)
(user_proc_price ?x_price)
(user_proc_work ?x_work)
(user_proc_W ?x_W)
(user_proc_size ?x_size)
(not(exists(cpu_struct (name ?x_name) (work ?x_work) (W ?x_W) (price ?x_price) (size ?x_size))))
?f_addr <- (user_want 1)
=>
(printout t crlf "Not founded cpu for you. =C" crlf);
(retract ?f_addr);
(assert (user_want 0));
);
