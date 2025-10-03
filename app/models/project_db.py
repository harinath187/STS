from .db import get_db_connection
import mysql.connector
from .db import get_db_connection
from app.utils.logger import logger

from flask import render_template

def get_today_task():
    conn = None
    cursor = None 
    try:   
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select task_id,task_name,task_description,concat(firstname,' ',lastname) as full_name,estimated_hrs,worked_hrs,Start_Date,Comments,status from project_task p join employee e on p.assigned_to = e.id where End_Date =CURDATE()
        """
        cursor.execute(query)
        due_today = cursor.fetchall()
        print("list of task due_today",due_today)
        logger.info(f"fteched {len(due_today)} Today_task")
        return due_today
    except Exception as e:
        logger.error(f"Error fetching project task: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:

            conn.close()

def get_all_task():
    conn = None
    cursor = None 
    try:   
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select task_id,task_name,task_description,concat(firstname,' ',lastname) as full_name,estimated_hrs,worked_hrs,Start_Date,Comments,status from project_task p join employee e on p.assigned_to = e.id 
        """
        cursor.execute(query)
        due_today = cursor.fetchall()
        print("list of task due_today",due_today)
        logger.info(f"fteched {len(due_today)} Today_task")
        return due_today
    except Exception as e:
        logger.error(f"Error fetching project task: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:

            conn.close()


def get_pending_task():
    conn = None
    cursor = None 
    try:   
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select task_id,task_name,task_description,concat(firstname,' ',lastname) as full_name,estimated_hrs,worked_hrs,Start_Date,Comments,status from project_task p join employee e on p.assigned_to = e.id where status="PENDING"
        """
        cursor.execute(query)
        due_today = cursor.fetchall()
        print("list of task due_today",due_today)
        logger.info(f"fteched {len(due_today)} Today_task")
        return due_today
    except Exception as e:
        logger.error(f"Error fetching project task: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:

            conn.close()    

def get_completed_task():
    conn = None
    cursor = None 
    try:   
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select task_id,task_name,task_description,concat(firstname,' ',lastname) as full_name,estimated_hrs,worked_hrs,Start_Date,Comments,status from project_task p join employee e on p.assigned_to = e.id where status="COMPLETED"
        """
        cursor.execute(query)
        due_today = cursor.fetchall()
        print("list of task due_today",due_today)
        logger.info(f"fteched {len(due_today)} Today_task")
        return due_today
    except Exception as e:
        logger.error(f"Error fetching project task: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:

            conn.close()      



def get_task_by_date(date):
    conn =None
    cursor = None
    try:   
        conn = get_db_connection()
        # print("input date",date)
        cursor = conn.cursor(dictionary=True)
        query = """
            select task_id,task_name,task_description,concat(firstname,' ',lastname) as full_name,estimated_hrs,worked_hrs,Start_Date,Comments,status from project_task p join employee e on p.assigned_to = e.id where End_Date = %s"""
    
        cursor.execute(query ,(date,))
        due_today = cursor.fetchall()
        print("list of task due_today",due_today)
        logger.info(f"fteched {len(due_today)} Today_task")
        return due_today
    except Exception as e:
        logger.error(f"Error fetching project task: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()    

def over_due_task():  
    conn =None
    cursor = None
    try:   
        conn = get_db_connection()
        
        cursor = conn.cursor(dictionary=True)
        query = """
            select task_id,task_name,task_description,concat(firstname,' ',lastname) as full_name,estimated_hrs,worked_hrs,Start_Date,Comments,status from project_task p join employee e on p.assigned_to = e.id where End_Date > CURDATE()"""
    
        cursor.execute(query )
        due_today = cursor.fetchall()
        print("list of task due_today",due_today)
        logger.info(f"fteched {len(due_today)} Today_task")
        return due_today
    except Exception as e:
        logger.error(f"Error fetching project task: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()    
          