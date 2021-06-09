import logging
from web.app.routes import notification
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
    conn = psycopg2.connect(dbname="techconfdb" user="udacityadmin@techconfdbserver", password = "Udacity@")
    cur = conn.cursor()

    try:
        # TODO: Get notification message and subject from database using the notification_id
        notification = cur.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))
        attendee_list = cur.execute("SELECT first_name, last_name, email FROM attendee;")
        for attendee in attendee_list:
            message = Mail(from_email='info@techconf.com',to_emails=attendee[2],subject=notification[1],plain_text_contents=notification[0])
            try:
                sg=SendGridAPIClient('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"')
                sg.send(message)
            except Exception as e:
                print(e.messsage)

        # TODO: Get attendees email and name

        # TODO: Loop through each attendee and send an email with a personalized subject

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection