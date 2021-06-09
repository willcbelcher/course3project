import logging
import azure.functions as func
import psycopg2-binary
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    conn = psycopg2.connect("dbname=techconfdb user=udacityadmin@techconfdbserver")
    cur = conn.cursor()

    try:
        # TODO: Get notification message and subject from database using the notification_id
        cur.execute("SELECT * FROM notification WHERE id = notification_id")
        logging.info('Here is cur.fetchone(): ', cur.fetchone())
        

        # TODO: Get attendees email and name

        # TODO: Loop through each attendee and send an email with a personalized subject

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection