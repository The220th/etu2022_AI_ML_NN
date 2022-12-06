;;;
;;; nPE)l(DE, 4EM HA4ATb 4uTATb KOD Hu)l(E OrPAHu4uTEJlbHOu JluHuu BHu3Y
;;; 3HAuTE, 4TO ABTOP ETOrO BblCEPA HE HECET OTBETCTBEHHOCTu 3A nCuXuKY
;;; 4uTAloWErO ETOT KOD. 
;;; OT nPO4TEHu9 TOrO, 4TO Hu)l(E, BO3MO)l(HA nOTEP9 MO3rA HACOBCEM!!!
;;;
;;;
;;;
;;;
;;;
;;;
;;;
;;;
;;;
;;;
;;; ================================================================================











(defglobal
?*ID* = 0

?*init_LU* = 5
?*init_CU* = 8
?*init_RU* = 3
?*init_LM* = 4
?*init_CM* = 0
?*init_RM* = 2
?*init_LD* = 7
?*init_CD* = 6
?*init_RD* = 1

?*goal_LU* = 1
?*goal_CU* = 2
?*goal_RU* = 3
?*goal_LM* = 4
?*goal_CM* = 5
?*goal_RM* = 6
?*goal_LD* = 7
?*goal_CD* = 8
?*goal_RD* = 0
);

; Шаблон узла
(deftemplate Node
(slot id(type NUMBER) (default 0)) ; индификатор

(slot LU (type NUMBER)) ; left up
(slot CU (type NUMBER)) ; center up
(slot RU (type NUMBER)) ; right up
(slot LM (type NUMBER)) ; left mid
(slot CM (type NUMBER)) ; center mid
(slot RM (type NUMBER)) ; right mid
(slot LD (type NUMBER)) ; left down
(slot CD (type NUMBER)) ; center down
(slot RD (type NUMBER)) ; right down

(slot g (type NUMBER)) ; cost, depth
(slot status(type NUMBER) (default 0)) ; статус вершины: 0 – не раскрыта, 1 – раскрыта, 2 – соответствует решению
(slot parent (type NUMBER)) ; ссылка на родителя
(slot f (type NUMBER)) ; значение целевой функции для данной вершины f = g + h
);

(deffunction get_next_ID()
(bind ?*ID* (+ ?*ID* 1)) ;; инкрементируем ID
?*ID*
);

(deffunction calc_f(?g
                    ?cur_LU ?cur_CU ?cur_RU
                    ?cur_LM ?cur_CM ?cur_RM
                    ?cur_LD ?cur_CD ?cur_RD)
(bind ?a ?g)
(if (not (= ?cur_LU ?*goal_LU*)) then (bind ?a (+ ?a 1)))
(if (not (= ?cur_CU ?*goal_CU*)) then (bind ?a (+ ?a 1)))
(if (not (= ?cur_RU ?*goal_RU*)) then (bind ?a (+ ?a 1)))
(if (not (= ?cur_LM ?*goal_LM*)) then (bind ?a (+ ?a 1)))
(if (not (= ?cur_CM ?*goal_CM*)) then (bind ?a (+ ?a 1)))
(if (not (= ?cur_RM ?*goal_RM*)) then (bind ?a (+ ?a 1)))
(if (not (= ?cur_LD ?*goal_LD*)) then (bind ?a (+ ?a 1)))
(if (not (= ?cur_CD ?*goal_CD*)) then (bind ?a (+ ?a 1)))
(if (not (= ?cur_RD ?*goal_RD*)) then (bind ?a (+ ?a 1)))
?a
);

; Изначальная "база знаний"
(deffacts initial
  (Node (id (get_next_ID))
        (LU ?*init_LU*) (CU ?*init_CU*) (RU ?*init_RU*) 
        (LM ?*init_LM*) (CM ?*init_CM*) (RM ?*init_RM*) 
        (LD ?*init_LD*) (CD ?*init_CD*) (RD ?*init_RD*)
        (g 0) (parent 0) 
        (f (calc_f 0 ?*init_LU* ?*init_CU* ?*init_RU* ?*init_LM* ?*init_CM* ?*init_RM* ?*init_LD* ?*init_CD* ?*init_RD*))
  )
  (min (calc_f 0 ?*init_LU* ?*init_CU* ?*init_RU* ?*init_LM* ?*init_CM* ?*init_RM* ?*init_LD* ?*init_CD* ?*init_RD*))
);

;;; EKCnEPT EKCnEPTA BuDuT u3DAJlEKA, 
;;; HOWA EKCnEPTA T9)l(EJlA, 
;;; A CEPDcE CDEJlAHO u3 nECKA...

(defrule test_goal
(declare (salience 500))

?f_addr <- (Node (id ?v_id) (LU ?v_LU) (CU ?v_CU) (RU ?v_RU)
                            (LM ?v_LM) (CM ?v_CM) (RM ?v_RM)
                            (LD ?v_LD) (CD ?v_CD) (RD ?v_RD)
                 (g ?v_g) (status ~2) (parent ?v_parent) (f ?v_f)
            )
(test (= ?v_LU ?*goal_LU*));
(test (= ?v_CU ?*goal_CU*));
(test (= ?v_RU ?*goal_RU*));
(test (= ?v_LM ?*goal_LM*));
(test (= ?v_CM ?*goal_CM*));
(test (= ?v_RM ?*goal_RM*));
(test (= ?v_LD ?*goal_LD*));
(test (= ?v_CD ?*goal_CD*));
(test (= ?v_RD ?*goal_RD*));
=>
(modify ?f_addr(status 2));
)

(defrule stop_if_no_solution
(declare (salience 200))

(not (Node(status 0|2)))
=>
(halt);
(printout t "No solution" crlf);
)

(defrule stop_if_solution_finded
(declare (salience 200))

(Node(status 2))
=>
(halt);
(printout t "fined solution" crlf);
)

;;; C ETOrO MOMEHTA BECb MuP - ETO EKCnEPTHblE CuCTEMbl. 
;;; Tbl EKCnEPT, 9 EKCnEPT, KOT EKCnEPT, CTOJl EKCnEPT...

(defrule find_min ;; определение текущего минимума ЦФ
(declare (salience 150))

?f_addr_min<-(min ?min)
(Node (f ?F&:(< ?F ?min)) (status 0)) ; Cуществование вершины, у которой
                                      ; значение целевой функции меньше текущего min
=>
(retract ?f_addr_min) ;
(assert (min ?F))     ; обновить min
)

;;; ECJlu ECTb BOnPOCbl,
;;; TO 3DECb PEWEHuE BCEX nPO6JlEM: https://i.imgur.com/4oDusdM.png

(defrule remove_repeats
(declare (salience 1000)) ;; максимальный приоритет

?f_addr_1 <- (Node (id ?v_id_1) (LU ?v_LU_1) (CU ?v_CU_1) (RU ?v_RU_1)
                                (LM ?v_LM_1) (CM ?v_CM_1) (RM ?v_RM_1)
                                (LD ?v_LD_1) (CD ?v_CD_1) (RD ?v_RD_1)
                 (g ?v_g_1) (status 0) (parent ?v_parent_1) (f ?v_f_1)
            )

?f_addr_2 <- (Node (id ?v_id_2&~?v_id_1) (LU ?v_LU_2) (CU ?v_CU_2) (RU ?v_RU_2)
                                         (LM ?v_LM_2) (CM ?v_CM_2) (RM ?v_RM_2)
                                         (LD ?v_LD_2) (CD ?v_CD_2) (RD ?v_RD_2)
                 (g ?v_g_2) (status 0) (parent ?v_parent_2) (f ?v_f_2)
            )
(test(= ?v_LU_1 ?v_LU_2))
(test(= ?v_CU_1 ?v_CU_2))
(test(= ?v_RU_1 ?v_RU_2))
(test(= ?v_LM_1 ?v_LM_2))
(test(= ?v_CM_1 ?v_CM_2))
(test(= ?v_RM_1 ?v_RM_2))
(test(= ?v_LD_1 ?v_LD_2))
(test(= ?v_CD_1 ?v_CD_2))
(test(= ?v_RD_1 ?v_RD_2))

(test(< ?v_f_1 ?v_f_2))
=>
(retract ?f_addr_2) ; удаление повторной вершины с большей ЦФ
)

;;; TODO: OTDOXHYTb OT ETOu nAPAWu, 
;;; A TO: https://i.imgur.com/bnlZS5j.png






