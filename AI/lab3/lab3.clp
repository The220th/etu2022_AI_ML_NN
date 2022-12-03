
(deftemplate cpu_struct "CPU struct"
  (slot name (type STRING))
  (slot work (type STRING) (allowed-values "min" "doc" "max" "server"))
  (slot W (type STRING) (allowed-values "low" "high"))
  (slot price (type STRING) (allowed-values "low" "high"))
  (slot size (type STRING) (allowed-values "small" "standard"))
);


(deffacts initial
  (cpu_struct (name "i5-3570") (work "min") (W "high") (price "low") (size "standard"));
  (cpu_struct (name "i5-9400") (work "max") (W "high") (price "high") (size "standard"));
  (cpu_struct (name "celeron 847") (work "doc") (W "low") (price "low") (size "small"));
  (cpu_struct (name "cortex-A53") (work "min") (W "low") (price "low") (size "small"));
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

(defrule R_if1_1
(user_want 1)
?f_addr <- (user_want 1)
=>
(printout t crlf "SHIT 1" crlf);
(retract ?f_addr);
(assert (user_want 0));
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
