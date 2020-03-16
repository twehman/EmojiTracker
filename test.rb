#!/usr/bin/env ruby

# A quick script to convert the XML from Android app "SMS Backup & Restore" into CSV.
#
# Usage: $ /workspace/project/sms-20191025143732.xml < PATH/TO/BACKUP/FILE.xml

require "nokogiri"
require "csv"

class Array
  def to_i
    self.map {|x| begin; Integer(x); rescue; nil; end}.compact
  end
end

input_array = ARGV
chars = input_array[0]
charray = Array.new(chars.split(//))
y = charray.to_i
x = y.join

# Specify the backup file's attributes and data types.
COLUMNS = { "protocol" => :to_i, "address" => :to_s, "date" => :to_i, "type" => :to_i, "subject" => :to_s, "body" => :to_s, "toa" => :to_i, "sc_toa" => :to_i, "service_center" => :to_s, "read" => :to_i, "status" => :to_i, "locked" => :to_i, "date_sent" => :to_s, "readable_date" => :to_s, "contact_name" => :to_s }

# Read backup file from stdin and into Nokogiri.
backup = Nokogiri::XML ARGF.read

# Pluck out just the SMS nodes
messages = backup.css("sms")

# For each message, grab and convert each attribute specified above.
rows = messages.map { |m| COLUMNS.map {|k,v| m.attribute(k).content.method(v).call }}

# Write the data as a CSV to stdout.
$stdout.reopen(x + "txts.csv", "w")
CSV do |txts|
	txts << COLUMNS.keys
	rows.each {|r| txts << r }
end